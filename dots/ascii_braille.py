# Dots - A braille translation program.
#
# Copyright (C) 2009 Eitan Isaacson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

ascii_to_braille = {
    u'\r': u'\r',
    u'\n': u'\n',
    u' ': u'\u2800',
    u'!': u'\u282e',
    u'"': u'\u2810',
    u'#': u'\u283c',
    u'$': u'\u282b',
    u'%': u'\u2829',
    u'&': u'\u282f',
    u"'": u'\u2804',
    u'(': u'\u2837',
    u')': u'\u283e',
    u'*': u'\u2821',
    u'+': u'\u282c',
    u',': u'\u2820',
    u'-': u'\u2824',
    u'.': u'\u2828',
    u'/': u'\u280c',
    u'0': u'\u2834',
    u'1': u'\u2802',
    u'2': u'\u2806',
    u'3': u'\u2812',
    u'4': u'\u2832',
    u'5': u'\u2822',
    u'6': u'\u2816',
    u'7': u'\u2836',
    u'8': u'\u2826',
    u'9': u'\u2814',
    u':': u'\u2831',
    u';': u'\u2830',
    u'<': u'\u2823',
    u'=': u'\u283f',
    u'>': u'\u281c',
    u'?': u'\u2839',
    u'@': u'\u2808',
    u'[': u'\u282a',
    u'\\': u'\u2833',
    u']': u'\u283b',
    u'^': u'\u2818',
    u'_': u'\u2838',
    u'a': u'\u2801',
    u'b': u'\u2803',
    u'c': u'\u2809',
    u'd': u'\u2819',
    u'e': u'\u2811',
    u'f': u'\u280b',
    u'g': u'\u281b',
    u'h': u'\u2813',
    u'i': u'\u280a',
    u'j': u'\u281a',
    u'k': u'\u2805',
    u'l': u'\u2807',
    u'm': u'\u280d',
    u'n': u'\u281d',
    u'o': u'\u2815',
    u'p': u'\u280f',
    u'q': u'\u281f',
    u'r': u'\u2817',
    u's': u'\u280e',
    u't': u'\u281e',
    u'u': u'\u2825',
    u'v': u'\u2827',
    u'w': u'\u283a',
    u'x': u'\u282d',
    u'y': u'\u283d',
    u'z': u'\u2835'}

braille_to_ascii = {
    u'\u2800': u' ',
    u'\u2801': u'a',
    u'\u2802': u'1',
    u'\u2803': u'b',
    u'\u2804': u"'",
    u'\u2805': u'k',
    u'\u2806': u'2',
    u'\u2807': u'l',
    u'\u2808': u'@',
    u'\u2809': u'c',
    u'\u280a': u'i',
    u'\u280b': u'f',
    u'\u280c': u'/',
    u'\u280d': u'm',
    u'\u280e': u's',
    u'\u280f': u'p',
    u'\u2810': u'"',
    u'\u2811': u'e',
    u'\u2812': u'3',
    u'\u2813': u'h',
    u'\u2814': u'9',
    u'\u2815': u'o',
    u'\u2816': u'6',
    u'\u2817': u'r',
    u'\u2818': u'^',
    u'\u2819': u'd',
    u'\u281a': u'j',
    u'\u281b': u'g',
    u'\u281c': u'>',
    u'\u281d': u'n',
    u'\u281e': u't',
    u'\u281f': u'q',
    u'\u2820': u',',
    u'\u2821': u'*',
    u'\u2822': u'5',
    u'\u2823': u'<',
    u'\u2824': u'-',
    u'\u2825': u'u',
    u'\u2826': u'8',
    u'\u2827': u'v',
    u'\u2828': u'.',
    u'\u2829': u'%',
    u'\u282a': u'[',
    u'\u282b': u'$',
    u'\u282c': u'+',
    u'\u282d': u'x',
    u'\u282e': u'!',
    u'\u282f': u'&',
    u'\u2830': u';',
    u'\u2831': u':',
    u'\u2832': u'4',
    u'\u2833': u'\\',
    u'\u2834': u'0',
    u'\u2835': u'z',
    u'\u2836': u'7',
    u'\u2837': u'(',
    u'\u2838': u'_',
    u'\u2839': u'?',
    u'\u283a': u'w',
    u'\u283b': u']',
    u'\u283c': u'#',
    u'\u283d': u'y',
    u'\u283e': u')',
    u'\u283f': u'='}
