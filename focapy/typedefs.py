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
             }

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
# format - final C header component to be written. Uses %VAR_CONTEXT_VARS%
#          and %%map_var%%.
#          %VAR_CONTEXT_VARS%:
#              %NAME%   - Variable name.

CUSTOM_TYPES = {
                'character' :
                            {
                                'regex':
                                        [ ## TODO: variable value support
                                            r'character\(len=(\d+)\)',
                                            r'character\*(\d+)',
                                        ],
                                'map'   :
                                        [
                                            'length=%INT%',
                                        ],
                                'format':   'char %NAME%[%%length%%]',
                            },
                'type'      :
                            {
                                'regex':
                                        [
                                            r'type\((\w+)\)',
                                        ],
                                'map'   :
                                        [
                                            'type_name=%STRING%',
                                        ],
                                'format':   '%%type_name%% %POINTER%%NAME%',
                            },
               }

# Override types - Override types are types that don't follow any rules,
# and require a manual override.
OVERRIDE_TYPES = {
                   #'integer(i_kind)'  : 'int',
                   #'real(r_single)'   : 'float',
                 }

