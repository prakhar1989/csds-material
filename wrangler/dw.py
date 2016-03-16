# Python run-time for Wrangler
#
# Creator: Sean Kandel
# Other contributors: Philip Guo

'''
TODOs:
	- Sorting of Date objects is not yet implemented


Performance notes:

- izip and other itertools might speed up iteration and reduce memory usage:

	http://www.scottkirkwood.com/2004/11/python-use-izip-for-iterating-over.html

- Run "python -O <args>" to disable asserts (might speed things up slightly)


Misc. notes:

- use this line to trigger the debugger:
		import pdb; pdb.set_trace()

- to run with the profiler, use:
		python -m cProfile <args>

'''

import re, math, itertools

# TODO: make these much more precise
date_RE1 = re.compile('\d+[.]\d+[.]\d+')
date_RE2 = re.compile('\d+[-]\d+[-]\d+')
date_RE3 = re.compile('\d+[/]\d+[/]\d+')


class DataWrangler(object):
	def __init__(self):
		self.transforms = []

	# apply a list of transforms on a table and return the resulting table
	def apply(self, table):
		table.mark_immutable() # for safety, to prevent accidental modification
		cur = table
		for t in self.transforms:
			cur = t.apply(cur)
		return cur

	# apply a list of transforms on a file and return the resulting table
	def apply_to_file(self, filename):
		# Optimization: if the first transform is to split by newlines, then
		# it seems wasteful to read the entire file into memory as a string and
		# then use re.split() to split by newlines ... special-case this common
		# transform to save time and memory!  e.g.,:
		'''
		dw.Split(column=["data"],
									 table=0,
									 status="active",
									 drop=True,
									 result="row",
									 update=False,
									 insert_position="right",
									 row=None,
									 on="\n",
									 before=None,
									 after=None,
									 ignore_between=None,
									 which=1,
									 max=0,
									 positions=None,
									 quote_character=None))
		'''
		first_transform = self.transforms[0]
		if (first_transform.name == 'split' and \
				first_transform['result'] == 'row' and \
				first_transform['on'] == '\n' and \
				first_transform['drop'] == True):
			t = Table()
			c = Column('data')
			# VERY IMPORTANT - open in 'rU' mode to enable
			# Universal newline support, so that we can properly
			# read files with Windows, Mac, or UNIX line endings
			# (see http://www.python.org/dev/peps/pep-0278/)
			for line in open(filename, 'rU'):
				c.append(line.rstrip('\n')) # cut off trailing newline
			t.insert_column(c)
			self.transforms.pop(0) # eliminate the first transform!

		# default behavior --- read the entire file into memory as a big string:
		else:
			input_file = open(filename, 'rU')
			input_text = input_file.read()
			t = Table()
			c = Column('data')
			c.set_data([input_text])
			t.insert_column(c)

		return self.apply(t)


	def apply_and_print_graphviz(self, table):
		print 'digraph {'
		table.mark_immutable() # for safety, to prevent accidental modification
		table.print_graphviz('Start')

		# keep around intermediate tables to make sure they're not GC'ed
		tbls = [table]
		for (i, t) in enumerate(self.transforms):
			tbls.append(t.apply(tbls[-1]))
			tbls[-1].print_graphviz('Step' + str(i+1) + '_' + t.name)
		print '}'

	def add(self, t):
		self.transforms.append(t)
		return self


'''
Performance notes:

	- row accesses might be slow since we're storing each column as a list

	- could consider simultaneously storing rows as well and keeping them
		in sync (although that might get gross and hairy)

	- NumPy arrays are fast but I think they must contain homogeneous
		elements (but perhaps we could just make everything a string?)
'''
class Table(object):
	def __init__(self):
		# ordered view of Columns
		self.data = []
		# can grab Columns by name as well
		self.data_by_name = {}
		self.name_counts = {}

		# this helps to prevent accidental modifications to Table objects
		self.is_immutable = False

	def copy(self):
		c = Table()
		# make shallow copies
		c.data = list(self.data)
		c.data_by_name = dict(self.data_by_name)
		c.name_counts = dict(self.name_counts)
		return c

	# like copy except create EMPTY versions of columns
	def copy_with_empty_cols(self):
		c = Table()
		for col in self:
			c.append_empty_column(col.name)
		return c
	
	def mark_immutable(self):
		self.is_immutable = True
		# sanity check --- make sure all columns have the same size
		num_elts = -1
		for e in self.data:
			if num_elts > 0:
				assert e.num_elts() == num_elts
			else:
				num_elts = e.num_elts()

	def clear(self):
		assert not self.is_immutable
		self.data = []
		self.name_counts = {}
		self.data_by_name = {}
	
	def remove_column(self, col):
		assert not self.is_immutable
		del self.data_by_name[col.name]
		self.data.remove(col)

	def append_empty_column(self, name):
		assert not self.is_immutable
		name = self.clean_name(name)
		col = Column(name)
		self.data.append(col)
		self.data_by_name[col.name] = col
		return col
	
	def finish_init_columns(self):
		assert not self.is_immutable
		num_elts = -1
		for e in self.data:
			e.finish_init()
			# sanity check --- make sure all columns have the same size
			if num_elts > 0:
				assert e.num_elts() == num_elts
			else:
				num_elts = e.num_elts()

	def insert_column(self, col, **options):
		assert not self.is_immutable
		col.name = self.clean_name(col.name)
		col.finish_init() # 'finalize' after changing column name (TODO: still kinda awkward)

		if 'index' in options:
			i = options['index']
			assert i >= 0
			self.data.insert(i, col)
		else:
			self.data.append(col)
		self.data_by_name[col.name] = col


	def clean_name(self, name):
		if name == None:
			name = '_'

		name = name.replace(' ', '_')

		# special rule for re-writing names that can be integers:
		try:
			x = int(name)
			name = '_' + name
		except ValueError:
			pass

		clean = name
		while(self[clean]!=None):
			try:			
				count = self.name_counts[name]
				self.name_counts[name] += 1
			except KeyError:
				count = 0
				self.name_counts[name]=1
			clean = name + str(self.name_counts[name])

		return clean


	def index(self, col):
		return self.data.index(col)


	# a bit inefficient, but avoids mutating column objects
	def set_name(self, col, name):
		assert not self.is_immutable
		col_idx = self.index(col)
		self.remove_column(col)

		new_name = self.clean_name(name)

		new_col = col.copy_with_new_name(new_name)
		self.insert_column(new_col, index=col_idx)


	# allow indexing of COLUMNS both by name and by numeric index
	def __getitem__(self, i):
		try:
			if(isinstance(i, str)):
				return self.data_by_name[i]
			else:
				return self.data[i]
		except KeyError:
			return None # TODO: silent failure might be bad

	def rows(self):
		if self.data:
			return self.data[0].num_elts()
		else:
			return 0

	def cols(self):
		return len(self.data)

	# access a specific row by numerical index
	# (if you want to iterate over ALL rows, use self.iter_rows())
	def row(self, r):
		return [c[r] for c in self.data]

	# iterate over all rows in table (memory-efficient)
	def iter_rows(self):
		for row_tuple in itertools.izip(*self.data):
			yield row_tuple

	def print_csv(self, filename=None):
		if filename:
			file_handle = open(filename, 'w')
		else:
			import sys
			file_handle = sys.stdout

		print >> file_handle, ','.join([c.name for c in self.data])

		for row_tuple in self.iter_rows():
			vals = ['"'+v.replace('"', '\\"') +'"' if v else '' for v in row_tuple]
			print >> file_handle, ','.join(vals)

	def print_tsv(self, filename=None):
		if filename:
			file_handle = open(filename, 'w')
		else:
			import sys
			file_handle = sys.stdout

		# print >> file_handle, '\t'.join([c.name for c in self.data])

		for row_tuple in self.iter_rows():
			vals = [v.replace('"', '\\"') if v else '' for v in row_tuple]
			print >> file_handle, '\t'.join(vals)


	def print_coljson(self, filename=None):
		print 'printing'
		if filename:
			file_handle = open(filename, 'w')
		else:
			import sys
			file_handle = sys.stdout
		
		print >> file_handle, 'var data = [' + ','.join(['{name: "' + c.name + '", type: "' + c.infer_type() + '", values: [' + ','.join([("'" + x.replace("'", "\\'") + "'") if Number().parse(x) == None else x for x in c])+ ']}\n' for c in self.data]) + ']'


	def print_coljson(self, filename=None):
		print 'printing'
		if filename:
			file_handle = open(filename, 'w')
		else:
			import sys
			file_handle = sys.stdout

		print >> file_handle, 'var data = [' + ','.join(['{name: "' + c.name + '", type: "' + c.infer_type() + '", values: [' + ','.join([("'" + x.replace("'", "\\'") + "'") if Number().parse(x) == None else x for x in c])+ ']}\n' for c in self.data]) + ']'


  # prints an HTML table with a given CSS classname
	def print_html(self, css_class='wrangler_tbl'):
		print '<table class="%s">' % css_class
		print '<tr>'
		# header row:
		for c in self.data:
			print '  <th>', c.name, '</th>'
		print '</tr>'

		for row_tuple in self.iter_rows():
			print '<tr>'
			for v in row_tuple:
				print '  <td>', v, '</td>'
			print '</tr>'
			
		print '</table>'

	# to debug memory layout and object sharing
	def print_graphviz(self, name):
		print '%s%d [label="%s", shape=ellipse]' % (name.replace(' ', ''), id(self), name)
		for c in self.data:
			print '%s%d->%s%d' % (name.replace(' ', ''), id(self), c.name, id(c))
			c.print_graphviz()


class Column(object):
	'''A Column object is immutable after its 'initialization'
	phase has ended, as indicated by a call to finish_init()

	Similarly, make it illegal to read from Column while it's still
	initializing

	This 'semi-immutability' property makes it easier to share Columns
	between Tables while making them easier to initialize
	'''
	def __init__(self, n, **options):
		# defaults:
		num_rows = 0
		t = 't'
		r = 'r'

		if 'num_rows' in options:
			num_rows = options['num_rows']
		if 'type' in options:
			t = options['type']
		if 'role' in options:
			r = options['role']

		self.name = n
		self.type = t
		self.role = r
		self.__data = [''] * num_rows # __ prefix means 'private'

		self.finished_init = False


	def finish_init(self):
		assert not self.finished_init
		self.finished_init = True

	def __getitem__(self, i):
		assert self.finished_init
		return self.__data[i]

	# sean did this so that it's more like JavaScript and doesn't give
	# out-of-bounds errors when appending
	def __setitem__(self, i, v):
		assert not self.finished_init
		l = len(self.__data)
		if(i >= l):
			for j in range(l, i+1):
				self.__data.append('')
		self.__data[i] = v

	def splice(self, i):
		assert not self.finished_init
		del self.__data[i]

	def append(self, v):
		assert not self.finished_init
		self.__data.append(v)

	def set_data(self, d):
		assert not self.finished_init
		self.__data = d

	def shift(self, direction, amt):
		assert not self.finished_init
		assert amt >= 0
		if direction == 'up':
			orig_size = len(self.__data)
			self.__data = self.__data[amt:] + ([''] * amt)
			assert len(self.__data) == orig_size
		else:
			assert direction == 'down'
			orig_size = len(self.__data)
			self.__data = (([''] * amt) + self.__data)[:orig_size]
			assert len(self.__data) == orig_size


	def gen_elts(self):
		assert self.finished_init
		for e in self.__data:
			yield e

	# makes a copy of __data
	def copy(self):
		assert self.finished_init
		c = Column(self.name, type=self.type, role=self.role)
		c.__data = list(self.__data) # copy!
		return c
	
	# makes a copy of self but sets the copy to have a different name
	def copy_with_new_name(self, new_name):
		c = self.copy()	# TODO: might be slow
		c.name = new_name
		return c

	# to debug memory layout and object sharing
	def print_graphviz(self):
		print '%s%d [label="%s\\n(%d rows)", shape=note]' % \
					(self.name, id(self), self.name, self.num_elts())

	# report column statistics
	def num_elts(self):
		return len(self.__data)

	def num_null_elts(self):
		n = 0
		for e in self.__data:
			if not e:
				n += 1
		return n

	def num_unique_elts(self):
		# don't count empty cells
		return len(set(e for e in self.__data if e))
	
	# returns a dict with the number of elements of each type:
	# 'number', 'date', 'string'
	def num_elts_by_type(self):
		d = {'number': 0, 'date': 0, 'string': 0}
		for val in self.__data:
			# skip over empty cells:
			if not val:
				continue

			# first look for dates
			if (date_RE1.match(val) or \
					date_RE2.match(val) or \
					date_RE3.match(val)):
				d['date'] += 1
				continue

			# then numbers
			try:
				float_val = float(val)
				d['number'] += 1
				continue
			except:
				pass

			# then default to string
			d['string'] += 1

		# sanity check
		assert sum(d.values()) + self.num_null_elts() == self.num_elts()

		return d
	

	def infer_type(self):
		d = self.num_elts_by_type()
		t = max(d, key=d.get)
		if(t=='number'):
			return 'numeric'
		if(t=='date'):
			return 'ordinal'
		if(t=='string'):
			return 'nominal'
	

	# does this column only contain values of ONE single type?
	# (don't count EMPTY columns as 'homogeneous')
	def is_homogeneous(self):
		lst = [e for e in self.num_elts_by_type().values() if e > 0]
		return len(lst) == 1


class Transform(object):
	'''
	The primary action for a Transform object is to apply itself on a
	table using:

	  def apply(self, table)
	
	which should produce a NEW table that is the result of applying the
	transform to 'table' (DO NOT mutate the original table, to facilitate
	easy undo/redo)
	'''
	def __init__(self, **options):
		self.parameters = options

	# TODO: I don't like this operator overloading, but it's already used everywhere ...
	def __getitem__(self, i):
		try:
			return self.parameters[i]
		except KeyError:
			return None

	def __setitem__(self, i, val):
		self.parameters[i] = val

	# only set k=v if it's NOT already been set
	def set_default(self, k, v):
		if k not in self.parameters:
			self.parameters[k] = v

	def get_selected_columns(self, table):
		col_names = self['column']
		# select ALL columns if none provided in transform
		if not col_names:
			col_names = [c.name for c in table]
		return [table[c] for c in col_names]

	# sub-classes must implement!
	def apply(self, table):
		raise NotImplementedError


class Map(Transform):
	def __init__(self, **options):
		super(Map,self).__init__(**options)

	def apply(self, table):
		table.mark_immutable() # for safety, to prevent accidental modification
		columns = self.get_selected_columns(table)
		assert columns

		update_index = table.index(columns[-1]) # use the FINAL selected column for update_index

		if self['result'] == 'row':
			new_table = table.copy_with_empty_cols()
			row_index = 0
			for values in itertools.izip(*columns):
				result = self.transform(values)
				num_extra_rows = len(result)
				for col in table:
					new_col = new_table[col.name]
					for i in range(num_extra_rows):
						if(col in columns):						
							new_col.append(result[i])
						else:
							new_col.append(col[row_index])
				row_index += 1						

			new_table.finish_init_columns()			
			return new_table
		else:
			assert self['result'] == 'column'

			num_rows = table.rows()
			table_copy = table.copy()

			if self['update']:
				# 'cut' and 'edit' transforms exercise this path

				new_cols = None

				for row_index in range(num_rows):
					# NOP if row doesn't pass the row condition test ...
					# will just use the original column's values since new_cols is
					# simply a copy of columns
					if self['row'] != None and (not self['row'].test(table, row_index)):
						continue

					result = self.transform([c[row_index] for c in columns])

					# if result is null, keep chuggin'
					if not result:
						continue

					if not new_cols:
						# COPY the original columns to the new columns, so that if we
						# don't map certain rows (e.g., in a selective mass edit),
						# then they will still have their original values
						new_cols = [c.copy() for c in columns]
						assert len(new_cols) == len(columns)

					assert len(new_cols) == len(result)
					for (new_col, res) in zip(new_cols, result):
						new_col[row_index] = res

				for (old_c, new_c) in zip(columns, new_cols):
					idx = table_copy.index(old_c)
					table_copy.remove_column(old_c)
					table_copy.insert_column(new_c, index=idx)
					assert new_c.num_elts() == num_rows # sanity check
			else:
				insert_position = table.cols() # by default, insert column at right-most end of table

				# insert column to the left/right of the current column's position if necessary
				if self['insert_position'] == 'right':
					insert_position = update_index + 1
				elif self['insert_position'] == 'left':
					insert_position = update_index

				new_cols = None
				for (row_index, values) in enumerate(itertools.izip(*columns)):
					result = self.transform(values)

					# if result is null, keep chuggin'
					if not result:
						continue

					if new_cols:
						# if a row splits into more columns than previous rows did,
						# then append new empty columns to the END of new_cols
						if len(result) > len(new_cols):
							for i in range(len(result) - len(new_cols)):
								new_cols.append(Column(self.name, num_rows=num_rows))
					else:
						# create new columns with the name of this transform
						new_cols = [Column(self.name, num_rows=num_rows) for e in result]
						assert new_cols

					for (c, r) in zip(new_cols, result):
						c[row_index] = r

				for i in range(len(new_cols)):
					table_copy.insert_column(new_cols[i], index=insert_position + i)
					assert new_cols[i].num_elts() == num_rows # sanity check

				# the finish ...
				if self['drop']:
					for col in columns:
						table_copy.remove_column(col)

			# careful with indentation!!!
			return table_copy


class Row(Transform):
	def __init__(self, **options):
		super(Row,self).__init__(**options)
		self.set_default('conditions', [])
		self.name = 'row'

	def test(self, tables, row):
		conditions = self['conditions']
		for cond in conditions:
			if(not cond.test(tables, row)):
				return False
		return True


class RowIndex(Transform):
	def __init__(self, **options):
		super(RowIndex,self).__init__(**options)
		self.set_default('indices', [])
		self.name = 'row_index'

	def test(self, tables, row):
		return row in self['indices']


class Empty(Transform):
	def __init__(self, **options):
		super(Empty,self).__init__(**options)
		self.name = 'empty'

	def test(self, table, row):
		for c in table:
			v = c[row]
			if(not v == None and len(str(v))):
				return False
		return True


class IsNull(Transform):
	def __init__(self, **options):
		super(IsNull,self).__init__(**options)
		self.name = 'is_null'

	def test(self, table, row):
		x = table[self['lcol']][row]
		return x == None or len(str(x)) == 0	


class IsType(Transform):
	def __init__(self, **options):
		super(IsType,self).__init__(**options)
		self.name = 'is_type'

	def test(self, table, row):
		return self['type'].parse(table[self['lcol']][row]) == None


class Type(Transform):
	def __init__(self, **options):
		super(Type,self).__init__(**options)
		self.name = 'type'

	def transform(self, values):
		return [self.parse(v) for v in values]

	def compare(self,a,b):
		a = self.parse(a)
		b = self.parse(b)
		if(a < b):
			return -1
		if(a==b):
			return 0
		if(a > b):
			return 1


class Number(Type):
	def __init__(self, **options):
		super(Number,self).__init__(**options)
		self.name = 'number'
		self.profiler_type = 'numeric'

	def parse(self, v):
		try:
			return float(v)
		except ValueError:
			return None

class Int(Type):
	def __init__(self, **options):
		super(Int,self).__init__(**options)
		self.name = 'int'
		self.profiler_type = 'numeric'

	def parse(self, v):
		try:
			return int(v)
		except ValueError:
			return None

class String(Type):
	def __init__(self, **options):
		super(String,self).__init__(**options)
		self.name = 'string'
		self.profiler_type = 'nominal'

	def parse(self, v):
		return v

class Date(Type):
	def __init__(self, **options):
		super(String,self).__init__(**options)
		self.name = 'string'
		self.profiler_type = 'ordinal'

	def parse(self, v):
		try:
			raise NotImplementedError
			return parser.parse(v) # TODO: use some Python date parser
		except ValueError:
			return None

class Eq(Transform):
	def __init__(self, **options):
		super(Eq,self).__init__(**options)
		self.name = 'eq'

	def test(self, table, row):
		return table[self['lcol']][row] == self['value']

class Neq(Transform):
	def __init__(self, **options):
		super(Neq,self).__init__(**options)
		self.name = 'neq'

	def test(self, table, row):
		return table[self['lcol']][row] != self['value']



class Contains(Transform):
	def __init__(self, **options):
		super(Contains, self).__init__(**options)
		self.name = 'contains'

	def test(self, table, row):
		return re.search(self['value'], str(table[self['lcol']][row]))

class StartsWith(Transform):
	def __init__(self, **options):
		super(StartsWith, self).__init__(**options)
		self.name = 'starts_with'

	def test(self, table, row):
		return re.match(self['value'], str(table[self['lcol']][row]))


class Filter(Transform):
	def __init__(self, **options):
		super(Filter,self).__init__(**options)
		self.set_default('row', Row())
		self.name = 'filter'

	def apply(self, table):
		table.mark_immutable() # for safety, to prevent accidental modification
		filtered_table = table.copy_with_empty_cols()
		row = self['row']
		for r in range(table.rows()):
			if(row.test(table, r)):
				pass
			else:
				for col in table:
					filtered_col = filtered_table[col.name]
					filtered_col.append(col[r])
		
		filtered_table.finish_init_columns()
		return filtered_table


class Fill(Transform):
	def __init__(self, **options):
		super(Fill,self).__init__(**options)
		self.set_default('direction', 'down')
		self.name = 'fill'

	def apply(self, table):
		table.mark_immutable() # for safety, to prevent accidental modification
		columns = self.get_selected_columns(table)

		start_row = 0
		end_row = table.rows()

		direction = self['direction']
		
		row = self['row']
		
		table_copy = table.copy()

		if direction=='down' or direction=='up':
			row_range = range(start_row, end_row)
			if direction == 'up':
				row_range.reverse()
			for col in columns:
				# create a new copy so that we don't mutate col
				filled_col = col.copy()

				fillValue = ''
				for r in row_range:
					v = col[r]
					if(v == None or v==''):
						filled_col[r] = fillValue
					else:
						if ((not row) or row.test(table, r)):
							fillValue = v
				
				# remove and insert at the SAME index
				idx = table.index(col)
				table_copy.remove_column(col)
				table_copy.insert_column(filled_col, index=idx)
		else:
			assert direction=='left' or direction=='right'
			# create new copies of columns so that we don't mutate originals
			filled_columns = [c.copy() for c in columns]

			col_range = range(0, len(columns))
			if direction == 'left':
				col_range.reverse()

			for r in range(start_row, end_row):
				if row and row.test(table, r):
					fillValue = ''
					for c in col_range:
						v = columns[c][r]
						if(v == None or v==''):
							filled_columns[c][r] = fillValue
						else:
							fillValue = v

			for (orig_col, filled_col) in zip(columns, filled_columns):
				# remove and insert at the SAME index
				idx = table.index(orig_col)
				table_copy.remove_column(orig_col)
				table_copy.insert_column(filled_col, index=idx)

		# careful with indentation!!!
		return table_copy


class Translate(Transform):
	'''TODO: implement support for translating 'left' and 'right'
	'''
	def __init__(self, **options):
		super(Translate,self).__init__(**options)
		self.set_default('direction', 'down') # can be 'up' or 'down'
		self.set_default('values', 1) # how many elements to shift up or down
		self.name = 'translate'

	def apply(self, table):
		table.mark_immutable() # for safety, to prevent accidental modification
		columns = self.get_selected_columns(table)

		shift_amount = self['values'] # weird name
		assert shift_amount >= 0
		
		table_copy = table.copy()

		for col in columns:
			# create a new copy so that we don't mutate col
			shifted_col = col.copy_with_new_name('translate')
			shifted_col.shift(self['direction'], shift_amount)
			assert shifted_col.num_elts() == col.num_elts()

			idx = table.index(col)
			table_copy.insert_column(shifted_col, index=idx + 1)

		# careful with indentation!!!
		return table_copy


class Transpose(Transform):
	def __init__(self, **options):
		super(Transpose,self).__init__(**options)
		self.name = 'transpose'

	def apply(self, table):
		table.mark_immutable() # for safety, to prevent accidental modification

		# TODO: how should we name the new transposed columns
		#       to match the JavaScript version's names?
		#
		# To REALLY give it a hard test, try transposing a table more
		# than once!!!

		transposed_cols = []
		for i in range(table.rows()):
			new_col = Column('transpose')
			new_col.set_data(table.row(i))
			transposed_cols.append(new_col)

		new_table = Table()
		for c in transposed_cols:
			new_table.insert_column(c)

		return new_table


class Fold(Transform):
	def __init__(self, **options):
		super(Fold,self).__init__(**options)
		self.set_default('drop', False)
		self.set_default('keys', [-1]) # the row numbers to use as fold keys
		self.name = 'fold'

	def apply(self, table):
		table.mark_immutable() # for safety, to prevent accidental modification
		columns = self.get_selected_columns(table)

		table_copy = table.copy()
		

		# These are the keys (row numbers) to use for the fold... we use the
		# header if the key = -1, otherwise we use the value in the cell at
		# the key's row
		keys = self['keys']

		key_values = []
		for col in columns:
			col_key_vals = []
			for key in keys:
				val = (col.name if key==-1 else col[key])
				col_key_vals.append(val)
			key_values.append(col_key_vals)

		foundLeft = False
		other_cols = []
		
		names = [c.name for c in columns]
		for col in table:
			if col.name in names:
				# only need to find the LEFT-MOST column:
				if not foundLeft:
					update_col = col
				foundLeft = True
			else:
				other_cols.append(col)

		assert update_col

		# kinda gross, but use append_empty_column to grab a unique name for
		# (possibly multiple) 'fold' columns:
		key_cols = [table_copy.append_empty_column('fold') for k in keys]
		value_col = table_copy.append_empty_column('value')
		other_cols = [Column(c.name) for c in other_cols]

		new_index = 0
		for r in range(table.rows()):
			if r not in keys:
				for k in range(len(columns)):
					for c in range(len(other_cols)):
						col = other_cols[c]
						col[new_index] = table[col.name][r]

					for j in range(len(key_cols)):
						key_cols[j][new_index] = key_values[k][j]

					value_col[new_index] = columns[k][r]
					new_index += 1

		updateIndex = table.index(update_col) if update_col else 0
		key_cols.append(value_col)

		table_copy.clear()
		# now insert original columns up until updateIndex, then insert
		# key_cols, then insert the rest of the original columns:
		for (i, col) in enumerate(other_cols):
			if i == updateIndex:
				for key_c in key_cols:
					table_copy.insert_column(key_c)
				key_cols = [] # empty it to prevent double insertion
			table_copy.insert_column(col)

		# insert at end if we haven't done it yet:
		if key_cols:
			for key_c in key_cols:
				table_copy.insert_column(key_c)

		return table_copy


class Unfold(Transform):
	def __init__(self, **options):
		super(Unfold,self).__init__(**options)
		self.set_default('drop', False)
		self.set_default('measure', [])
		self.set_default('column', [])
		self.name = 'Unfold'

	def apply(self, table):
		table.mark_immutable() # for safety, to prevent accidental modification
		columns = self.get_selected_columns(table)
		
		measure_column = table[self['measure']]
		
		new_column_headers = []
		header_column = columns[0]

		for v in header_column.gen_elts():
			if v not in new_column_headers:
				new_column_headers.append(v)

		key_columns = filter(lambda x: x.name not in [measure_column.name, header_column.name], table)

		reduction = {}
		reduction_index = 0

		new_table = Table()
		
		for col in key_columns:
			new_table.append_empty_column(col.name)
		
		# this name lookup is needed since table implementation changes names
		# under certain circumstances
		name_lookup = {}
		for header in new_column_headers:
			col = new_table.append_empty_column(header)
			name_lookup[header] = col.name

		for r in range(table.rows()):
			key = '*'.join([col[r] for col in key_columns])
			if key not in reduction:
				reduction[key] = reduction_index

				for col in key_columns:
					new_table[col.name][reduction_index] = col[r]

				reduction_index += 1

			index = reduction[key]
			header = header_column[r]
			measure = measure_column[r]

			new_table[name_lookup[header]][index] = measure

		# make all the resulting columns have the same size, filling in with
		# '' (blanks) as necessary
		max_elts = 0
		for c in new_table.data:
			max_elts = max(max_elts, c.num_elts())

		for c in new_table.data:
			# important guard condition so that we don't clobber columns that
			# are actually max_elts in length
			if c.num_elts() < max_elts:
				c[max_elts - 1] = '' # 'stretches' column to max_elts elements

		new_table.finish_init_columns()
		return new_table


class Drop(Transform):
	def __init__(self, **options):
		super(Drop,self).__init__(**options)
		self.set_default('drop', True)
		self.name = 'drop'

	def apply(self, table):
		table.mark_immutable() # for safety, to prevent accidental modification
		columns = self.get_selected_columns(table)

		table_copy = table.copy()
		
		if(self['drop']):
			for col in columns:
				table_copy.remove_column(col)

		return table_copy


class SetName(Transform):
	def __init__(self, **options):
		super(SetName,self).__init__(**options)
		self.set_default('drop', True)
		self.name = 'SetName'

	def apply(self, table):
		table.mark_immutable() # for safety, to prevent accidental modification
		columns = self.get_selected_columns(table)

		if self['header_row'] != None: # careful, header_row could be the number 0!
			# this is used to promote a row to be the column header

			row_num = self['header_row']

			new_table = Table()
			for c in table:
				copied_col = c.copy()
				val = c[row_num]
				if val == None or val == '':
					val = 'undefined'

				if self['drop']:
					copied_col.splice(row_num)

				new_table.insert_column(copied_col)
				new_table.set_name(copied_col, val)

			return new_table
		else:
			table_copy = table.copy()
			# TODO: does this work properly when we have more than 1 column?
			for (col, name) in zip(columns, self['names']):
				table_copy.set_name(col, name)
			return table_copy


class Sort(Transform):
	def __init__(self, **options):
		super(Sort,self).__init__(**options)
		self.set_default('direction', []) # 'asc' or 'desc'
		self.set_default('as_type', [])

	def apply(self, table):
		table.mark_immutable() # for safety, to prevent accidental modification
		columns = self.get_selected_columns(table)

		new_table = Table()

		types = self['as_type']
		assert types
		directions = [d for d in self['direction']]

		for d in range(len(self['direction']), len(columns)):
			directions.append('asc')
				
		directions = [(1 if d=='asc' else -1) for d in directions]

		assert len(directions) == len(types) == len(columns)

		# TODO: this is not well-tested
		def sort_fn(a, b):
			for i in range(0, len(columns)):
				col = columns[i]
				result = types[i].compare(col[a], col[b])
				if not result == 0:
					return directions[i]*result

			if(a<b):
				return -1
			if(a==b):
				return 0
			return 1
		
		sorted_rows = range(0, table.rows())
		sorted_rows.sort(sort_fn)

		results = [columns[0][i] for i in sorted_rows]

		new_table = table.copy_with_empty_cols()

		for c in range(table.cols()):
			column = table[c]
			new_column = new_table[c]
			for r in range(table.rows()):
				new_column[r] = column[sorted_rows[r]]

		new_table.finish_init_columns()
		return new_table


class Split(Map):
	def __init__(self, **options):
		super(Split,self).__init__(**options)
		self.set_default('update', False)
		self.set_default('drop', True)
		self.set_default('result', 'column')
		self.name = 'split'

	def transform(self, values):
		val = str(values[0])
		if(not val):
			return []

		max_splits = self['max']

		#Shortcut for big splits
		if (max_splits==0 and \
				self['on']!=None and \
				self['before']==None and \
				self['after']==None and \
				self['ignore_between'] == None and \
				self['quote_character'] == None):
			# hack to clean up trailing newlines before doing an re.split:
			if self['on'] == '\n':
				val = val.rstrip('\n')
			return re.split(self['on'], val)

		# TODO: haven't tested this path yet
		splits = match(val, {'on':self['on'],
												 'before':self['before'],
												 'after':self['after'],
												 'ignore_between':self['ignore_between'],
 												 'quote_character':self['quote_character'],
												 'max':self['max'],
												 'positions':self['positions']})
		splitValues = []

		for i in range(0,len(splits)):
			if(i%2==0):
				splitValues.append(splits[i])
		
		return splitValues

		
class Extract(Map):
	def __init__(self, **options):
		super(Extract,self).__init__(**options)
		self.set_default('update', False)
		self.set_default('drop', False)
		self.set_default('result', 'column')
		self.name = 'extract'

	def transform(self, values):
		val = str(values[0])
		splits = match(val,
									{'on':self['on'],
									 'before':self['before'],
									 'after':self['after'],
									 'ignore_between':self['ignore_between'],
									 'quote_character':self['quote_character'],
									 'max':self['max'],
									 'positions':self['positions']})

		splitValues = []
		
		for i in range(0,len(splits)):
			if(i%2==1):
				splitValues.append(splits[i])

		return splitValues


class Cut(Map):
	def __init__(self, **options):
		super(Cut,self).__init__(**options)
		self.set_default('update', True)
		self.set_default('drop', False)
		self.set_default('result', 'column')
		self.name = 'cut'

	def transform(self, values):
		splitValues = []
		for i in range(0, len(values)):
			v = values[i]
			val = str(v)
			splits = match(val,
									  {'on':self['on'],
										 'before':self['before'],
										 'after':self['after'],
										 'ignore_between':self['ignore_between'],
 										 'quote_character':self['quote_character'],
										 'max':self['max'],
										 'positions':self['positions']})
		
			x = ''
			for i in range(0,len(splits)):
				if(i%2==0):
					x += (splits[i])
			
			splitValues.append(x)

		return splitValues


class Merge(Map):
	def __init__(self, **options):
		super(Merge,self).__init__(**options)
		self.set_default('update', False)
		self.set_default('drop', False)
		self.set_default('result', 'column')
		self.set_default('glue', '') # use '' as default glue if none provided
		self.name = 'merge'

	def transform(self, values):
		merged_str = self['glue'].join(values)
		return [merged_str] # need to return a singleton list


# helper functions for edit transform:
def edit_capitalize(s):
	return ' '.join([e[0].upper() + e[1:] for e in s.split()])

def edit_uncapitalize(s):
	return ' '.join([e[0].lower() + e[1:] for e in s.split()])

def edit_upper(s):
	return s.upper()

def edit_lower(s):
	return s.lower()


class Edit(Map):
	'''
	Support cell editing or mass editing of a group of cells
	'''
	def __init__(self, **options):
		super(Edit,self).__init__(**options)
		self.set_default('update_method', None)
		self.set_default('to', None)
		self.name = 'edit'

	def transform(self, values):
		if self['to'] != None:
			return [self['to'] for v in values]
		else:
			assert self['update_method'] != None

			if self['update_method'] == "CAPITALIZE":
				edit_func = edit_capitalize
			elif self['update_method'] == "UNCAPITALIZE":
				edit_func = edit_uncapitalize
			elif self['update_method'] == "LOWER":
				edit_func = edit_lower
			elif self['update_method'] == "UPPER":
				edit_func = edit_upper
			else:
				assert False
			return [edit_func(v) for v in values]


def match(value, options):
	if(not value):
		return []
	
	max_splits = options['max']

	if(max_splits==None):
		max_splits = 1

	if (options['positions']!=None):
		pos = options['positions']
		if len(pos) == 1:
			return value[:pos[0]], value[pos[0]:pos[0]], value[pos[0]:]
		else:
			assert len(pos) == 2
			assert pos[0] <= pos[1]
			return value[:pos[0]], value[pos[0]:pos[1]], value[pos[1]:]

	if(options['ignore_between'] == None and options['quote_character'] != None):
		qc = options['quote_character']
		options['ignore_between'] = qc+'[^'+qc+']*'+qc


	#Shortcut for big splits
	if(options['on']!=None and options['before']==None and options['after']==None and options['ignore_between'] == None):
		if(max_splits==0):
			return re.split("(" + options['on'] + ")", value)

	remainder_to_split = value
	splits = []
	numSplit = 0
	while(max_splits <= 0 or numSplit < max_splits*1):
		s = match_once(remainder_to_split, options)

		if(len(s) > 1):
			remainder_to_split = s[2]
			splits.append(s[0])
			splits.append(s[1])
			occurrence = 0
		else:
			break
			
		numSplit+=1
	
	splits.append(remainder_to_split)
	occurrence = 0
	newSplits = []
	prefix = ''
	which = 1
	for i in range(0, len(splits)):
		if(i%2==1):
			occurrence+=1
			if(occurrence==which):
				newSplits.append(prefix)
				newSplits.append(splits[i])
				occurrence = 0
				prefix = ''
				continue

		prefix += splits[i]

	newSplits.append(prefix)
	return newSplits

	
def match_once(value, options):
	splits = []
	on = options['on']
	before = options['before']
	after = options['after']
	ignore_between = options['ignore_between']
	
	remainder = value
	remainder_offset = 0
	start_split_offset = 0
	add_to_remainder_offset = 0
	
	while(len(remainder)):
		valid_split_region = remainder
		valid_split_region_offset = 0
		start_split_offset = remainder_offset
		if(ignore_between):
			match = re.search(ignore_between, remainder)
			if(match):
				valid_split_region = valid_split_region[0:match.start(0)]
				remainder_offset += match.start(0) + len(match.group(0))
				remainder = remainder[match.start(0)+len(match.group(0)):]
			else:
				remainder = ''
		else:
			remainder = ''
	
		if(after):
			match = re.search(after, valid_split_region)
			if(match):
				valid_split_region_offset = match.start(0)+len(match.group(0))
				valid_split_region = valid_split_region[valid_split_region_offset:]
			else:
				continue
		if(before):
			match = re.search(before, valid_split_region)
			if(match):
				valid_split_region = valid_split_region[0:match.start(0)]
			else:
				continue

		match = re.search(on, valid_split_region)
		
		if(match):
			split_start = start_split_offset + valid_split_region_offset+match.start(0)
			split_end = split_start + len(match.group(0))

			splits.append(value[0:split_start])
			splits.append(value[split_start:split_end])			
			splits.append(value[split_end:])
			return splits

		else:	
			continue

	return [{'start':0, 'end':len(value), 'value':value}]


# Options for vim text editor:
# vim: set noexpandtab :
