#!/usr/bin/env python3

#########################################################################
#
#   This module adds Perl-style transliterations (i.e. tr/// or y///) to
#   Python 3, as well as the s/// syntax for specifying regular
#   expression substitutions.
#
#   Copyright 2009 David Liang
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#   Revisions:
#   2009-09-10  File created
#
#########################################################################

import re

class StringTransform:

    from codecs import decode
    from collections import defaultdict

    _re_alnum = re.compile(r'[A-Za-z0-9]')
    _re_translit_range = re.compile(r'(.)-(.)', re.DOTALL)
    _re_char_run = re.compile(r'(.)\1+', re.DOTALL)

    class ParseError(Exception):
        def __init__(self, *args):
            self.args = args

    def __init__(self):
        self.clear()

    def clear(self):
        self.ops = []

    def addSubstitution(self, pat, sub, opts):
        invalid = re.search(r'[^ailmsxg\d]', opts)
        if invalid:
            raise self.ParseError( "invalid regular expression flag",
                                   invalid.group() )
        flags = 0
        count = 1
        if 'a' in opts: flags |= re.A
        if 'i' in opts: flags |= re.I
        if 'l' in opts: flags |= re.L
        if 'm' in opts: flags |= re.M
        if 's' in opts: flags |= re.S
        if 'x' in opts: flags |= re.X
        if 'g' in opts:
            count = 0
        else:
            num = re.search(r'\d+', opts)
            if num:
                count = int(num.group())
        try:
            regex = re.compile(pat, flags)
        except re.error as e:
            raise self.ParseError(*e.args)

        if pat or sub:
            self.ops.append((regex, sub, count))


    @classmethod
    def ordinalsList(cls, str):
        list = []
        while str:
            run = cls._re_translit_range.match(str)
            if run:
                start, end = (ord(c) for c in run.group(1, 2))
                if start > end:
                    raise cls.ParseError(
                              "invalid range in transliteration operator",
                              run.group(0) )
                while start <= end:
                    list.append(start)
                    start += 1
                str = str[3:]
            else:
                list.append(ord(str[0]))
                str = str[1:]
        return list

    @staticmethod
    def complementList(ords, length):
        list = []
        ords = set(ords)
        i = 0
        while len(list) < length:
            if i not in ords:
                list.append(i)
            i += 1
        return list

    @classmethod
    def squash(cls, string):
        return cls._re_char_run.sub(r'\1', string)


    def addTransliteration(self, chars, repl, opts):
        invalid = re.search(r'[^cds]', opts)
        if invalid:
            raise self.ParseError( "invalid transliteration flag",
                                   invalid.group() )
        complm, delete, squash = 'c' in opts, 'd' in opts, 's' in opts
        try:
            chars = self.decode(chars.encode(), 'unicode_escape')
            repl  = self.decode(repl.encode(),  'unicode_escape')
        except UnicodeDecodeError as e:
            raise self.ParseError( "'%s' codec can't decode position %d-%d"
                                   % (e.encoding, e.start, e.end), e.reason )
        char_a = self.ordinalsList(chars)
        repl_a = self.ordinalsList(repl)
        if complm:
            char_a = self.complementList(char_a, len(repl_a))

        map = dict()
        if delete:
            default = ''
            if complm:
                map = self.defaultdict(lambda: default)
        elif repl_a:
            default = repl_a[-1]
            if complm:
                map = self.defaultdict(lambda: default)
        else:
            repl_a = char_a

        for i, c in enumerate(char_a):
            if c in map: continue
            try:
                map[c] = repl_a[i]
            except IndexError:
                map[c] = default

        if not complm:
            if not chars:
                return
            elif not squash:
                self.ops.append(map)
                return
        try:
            chars = chars.replace('[', r'\[').replace(']', r'\]')
            if complm:
                regex = re.compile( ('[^'+chars+']' if chars else '.') + '+',
                                    re.DOTALL )
            else:
                regex = re.compile('['+chars+']+')

        except re.error as e:
            raise self.ParseError(*e.args)

        if squash:
            sub = lambda m: self.squash(m.group().translate(map))
        else:
            sub = lambda m: m.group().translate(map)

        self.ops.append((regex, sub, 0))
        return


    def addOperation(self, expr):
        expr = expr.strip()
        if not expr:
            return
        elif expr.startswith('s'):
            op = 's'
        elif expr.startswith('y') or expr.startswith('tr'):
            op = 'y'
        else:
            raise self.ParseError("unrecognized operation", expr)

        i = (2 if expr.startswith('tr') else 1)
        if not expr[i:]:
            raise self.ParseError("unterminated expression", expr)
        elif self._re_alnum.match(expr[i]):
            raise self.ParseError("invalid delimiter", expr)

        sep = (r'\\' if expr[i] == '\\' else expr[i])
        mat = re.match( r'((?:\\.|[^\\'+sep+'])*)[' + sep + ']'
                        r'((?:\\.|[^\\'+sep+'])*)[' + sep + '](.*)',
                        expr[i+1:] )
        if not mat:
            raise self.ParseError("unterminated expression", expr)
        elif op == 's':
            self.addSubstitution(*mat.groups(''))
        elif op == 'y':
            self.addTransliteration(*mat.groups(''))


    def transform(self, string):
        for op in self.ops:
            if type(op) == tuple:
                string = op[0].sub(op[1], string, op[2])
            else:
                string = string.translate(op)
        return string



if __name__ == '__main__':

    import sys, os

    __prog__ = os.path.basename(sys.argv[0])
    __debugging__ = '-d' in sys.argv

    def Debug(*args):
        if __debugging__:
            print(*args, file=sys.stderr)

    if __debugging__:
        sys.argv.remove('-d')

    if len(sys.argv) == 1:
        sys.exit(2)

    try:
        st = StringTransform()
        for arg in sys.argv[1:]:
            st.addOperation(arg)

    except StringTransform.ParseError as e:
        print(__prog__, *e.args, sep=': ', file=sys.stderr)
        sys.exit(1)

    for line in sys.stdin:
        print(st.transform(line), end='')

