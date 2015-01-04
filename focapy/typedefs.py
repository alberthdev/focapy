#!/usr/bin/env python
# FoCaPy - Fortran to C and Python Wrapper
# Copyright 2014 Albert Huang.
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the Free
# Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307 USA
# 
# Type Definition Constants
# 

# Default types - types that follow the general SOMETYPE(SPEC) or
# SOMETYPE*SPEC rule.

DEFAULT_TYPES  = {
                    'byte'              : 'unsigned char',
                    'integer'           : 'int',
                    'real'              : 'float',

                    'double precision'  : 'double',
                    'logical'           : 'int',
                    'character'         : 'char',
                   #'some_ptr'          : ('c_ptr_type', '*'),
                 }

# Type table - Table for types that follow the general SOMETYPE(SPEC)
# or SOMETYPE*SPEC rule. The table specifies the SPEC portion of the
# type definition.

TYPE_TABLE = {
                'integer'   :
                                {
                                    1           : 'unsigned char',
                                    2           : 'short int',
                                    3           : 'int',
                                    4           : 'long long int',
                                    'i_kind'    : 'int',
                                    'i_byte'    : 'unsigned char',
                                    'i_short'   : 'short int',
                                    'i_long'    : 'int',
                                    'i_llong'   : 'long long int',
                                },
                'real'      :
                                {
                                    4           : 'float',
                                    8           : 'double',
                                    16          : 'long double',
                                    'r_kind'    : 'double',
                                    'r_single'  : 'float',
                                    'r_double'  : 'double',
                                    'r_quad'    : 'long double',
                                },
               #'some_ptr'  :   {   'ptr'       : ('c_ptr_type', '*'), },
             }

# Build lookup table
LOOKUP_TABLE = {}
for f_type in DEFAULT_TYPES:
    LOOKUP_TABLE[f_type] = DEFAULT_TYPES[f_type]

for f_base_type in TYPE_TABLE:
    for f_sub_type in TYPE_TABLE[f_base_type]:
        LOOKUP_TABLE[f_base_type + "(" + str(f_sub_type) + ")"] = TYPE_TABLE[f_base_type][f_sub_type]

# Fortran C type table
FORTRAN_DEFAULT_TYPES = {
                    'byte'              : 'INTEGER(C_SIGNED_CHAR)',
                    'integer'           : 'INTEGER(C_INT)',
                    'real'              : 'INTEGER(C_FLOAT)',

                    'double precision'  : 'REAL(C_DOUBLE)',
                    'logical'           : 'INTEGER(C_INT)',
                    'character'         : 'CHARACTER(C_CHAR)',
                   #'some_ptr'          : ('c_ptr_type', '*'),
                 }

FORTRAN_TYPE_TABLE = {
                'integer'   :
                                {
                                    1           : 'INTEGER(C_SHORT)',
                                    2           : 'INTEGER(C_INT)',
                                    3           : 'INTEGER(C_LONG)',
                                    4           : 'INTEGER(C_LONG_LONG)',
                                    'i_kind'    : 'INTEGER(C_INT)',
                                    'i_byte'    : 'INTEGER(C_SIGNED_CHAR)',
                                    'i_short'   : 'INTEGER(C_SHORT)',
                                    'i_long'    : 'INTEGER(C_INT)',
                                    'i_llong'   : 'INTEGER(C_LONG_LONG)',
                                },
                'real'      :
                                {
                                    4           : 'REAL(C_FLOAT)',
                                    8           : 'REAL(C_DOUBLE)',
                                    16          : 'REAL(C_LONG_DOUBLE)',
                                    'r_kind'    : 'REAL(C_DOUBLE)',
                                    'r_single'  : 'REAL(C_FLOAT)',
                                    'r_double'  : 'REAL(C_DOUBLE)',
                                    'r_quad'    : 'REAL(C_LONG_DOUBLE)',
                                },
               #'some_ptr'  :   {   'ptr'       : ('c_ptr_type', '*'), },
             }

# Build lookup table
FORTRAN_LOOKUP_TABLE = {}
for f_type in FORTRAN_DEFAULT_TYPES:
    FORTRAN_LOOKUP_TABLE[f_type] = FORTRAN_DEFAULT_TYPES[f_type]
##### TODO: do kinds? INTEGER(kind=??)
for f_base_type in FORTRAN_TYPE_TABLE:
    for f_sub_type in FORTRAN_TYPE_TABLE[f_base_type]:
        FORTRAN_LOOKUP_TABLE[f_base_type + "(" + str(f_sub_type) + ")"] = FORTRAN_TYPE_TABLE[f_base_type][f_sub_type]

# Generic regex - Generic regex for regular default types.
GENERIC_REGEX  = [
                    r'\((\w+)\)',
                    r'\*(\w+)',
                 ]

# Custom types - types that do not follow the standard format, but still
# have a custom format that can be used.
# 
# Format:
# regex  - the regex to match the Fortran type.
# map    - a mapping of each regex match to a named variable, respectively
#          by array. Format: map_var = %TYPE_VAR%. Uses %TYPE_VARS%:
#              %INT%    - Match integer type.
#              %STRING% - Match string type.
# type   - final C type.
# name   - final C variable name. Uses %VAR_CONTEXT_VARS% and %%map_var%%.
#          %VAR_CONTEXT_VARS%:
#              %NAME%   - Variable name.

CUSTOM_TYPES = {
                'character' :
                            {
                                'regex'     :
                                            [ ## TODO: variable value support
                                                r'character\(len=(\d+)\)',
                                                r'character\*(\d+)',
                                            ],
                                'map'       :
                                            [
                                                'length=%INT%',
                                            ],
                                'type'      :   'char',
                                'name'      :   '%NAME%[%%length%%]',
                                'pointer'   :   '',
                            },
                'type' :
                            {
                                'regex'     :
                                            [
                                                r'type\((\w+)\)',
                                            ],
                                'map'       :
                                            [
                                                'type_name=%STRING%',
                                            ],
                                'type'      : '%%type_name%%',
                                'name'      : '%NAME%',
                                'pointer'   : '',
                            },
               }

# Override types - Override types are types that don't follow any rules,
# and require a manual override.
OVERRIDE_TYPES = {
                   #'integer(i_kind)'  : 'int',
                   #'real(r_single)'   : 'float',
                   #'some_ptr'         : ('c_ptr_type', '*'),
                 }

