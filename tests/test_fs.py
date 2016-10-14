# coding: utf-8
"""
Base class for tests.

All Filesystems should be able to pass these.

"""

from __future__ import unicode_literals

import collections
from datetime import datetime
import io
import json
import math
import time

import fs.copy
import fs.move
from fs import ResourceType
from fs import errors
from fs import walk
from fs.opener import open_fs
from fs.subfs import SubFS

import pytz
import six
from six import text_type


UNICODE_TEXT = """

UTF-8 encoded sample plain-text file
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾

Markus Kuhn [ˈmaʳkʊs kuːn] &lt;mkuhn@acm.org> — 1999-08-20


The ASCII compatible UTF-8 encoding of ISO 10646 and Unicode
plain-text files is defined in RFC 2279 and in ISO 10646-1 Annex R.


Using Unicode/UTF-8, you can write in emails and source code things such as

Mathematics and Sciences:

  ∮ E⋅da = Q,  n → ∞, ∑ f(i) = ∏ g(i), ∀x∈ℝ: ⌈x⌉ = −⌊−x⌋, α ∧ ¬β = ¬(¬α ∨ β),

  ℕ ⊆ ℕ₀ ⊂ ℤ ⊂ ℚ ⊂ ℝ ⊂ ℂ, ⊥ &lt; a ≠ b ≡ c ≤ d ≪ ⊤ ⇒ (A ⇔ B),

  2H₂ + O₂ ⇌ 2H₂O, R = 4.7 kΩ, ⌀ 200 mm

Linguistics and dictionaries:

  ði ıntəˈnæʃənəl fəˈnɛtık əsoʊsiˈeıʃn
  Y [ˈʏpsilɔn], Yen [jɛn], Yoga [ˈjoːgɑ]

APL:

  ((V⍳V)=⍳⍴V)/V←,V    ⌷←⍳→⍴∆∇⊃‾⍎⍕⌈

Nicer typography in plain text files:

  ╔══════════════════════════════════════════╗
  ║                                          ║
  ║   • ‘single’ and “double” quotes         ║
  ║                                          ║
  ║   • Curly apostrophes: “We’ve been here” ║
  ║                                          ║
  ║   • Latin-1 apostrophe and accents: '´`  ║
  ║                                          ║
  ║   • ‚deutsche‘ „Anführungszeichen“       ║
  ║                                          ║
  ║   • †, ‡, ‰, •, 3–4, —, −5/+5, ™, …      ║
  ║                                          ║
  ║   • ASCII safety test: 1lI|, 0OD, 8B     ║
  ║                      ╭─────────╮         ║
  ║   • the euro symbol: │ 14.95 € │         ║
  ║                      ╰─────────╯         ║
  ╚══════════════════════════════════════════╝

Greek (in Polytonic):

  The Greek anthem:

  Σὲ γνωρίζω ἀπὸ τὴν κόψη
  τοῦ σπαθιοῦ τὴν τρομερή,
  σὲ γνωρίζω ἀπὸ τὴν ὄψη
  ποὺ μὲ βία μετράει τὴ γῆ.

  ᾿Απ᾿ τὰ κόκκαλα βγαλμένη
  τῶν ῾Ελλήνων τὰ ἱερά
  καὶ σὰν πρῶτα ἀνδρειωμένη
  χαῖρε, ὦ χαῖρε, ᾿Ελευθεριά!

  From a speech of Demosthenes in the 4th century BC:

  Οὐχὶ ταὐτὰ παρίσταταί μοι γιγνώσκειν, ὦ ἄνδρες ᾿Αθηναῖοι,
  ὅταν τ᾿ εἰς τὰ πράγματα ἀποβλέψω καὶ ὅταν πρὸς τοὺς
  λόγους οὓς ἀκούω· τοὺς μὲν γὰρ λόγους περὶ τοῦ
  τιμωρήσασθαι Φίλιππον ὁρῶ γιγνομένους, τὰ δὲ πράγματ᾿
  εἰς τοῦτο προήκοντα,  ὥσθ᾿ ὅπως μὴ πεισόμεθ᾿ αὐτοὶ
  πρότερον κακῶς σκέψασθαι δέον. οὐδέν οὖν ἄλλο μοι δοκοῦσιν
  οἱ τὰ τοιαῦτα λέγοντες ἢ τὴν ὑπόθεσιν, περὶ ἧς βουλεύεσθαι,
  οὐχὶ τὴν οὖσαν παριστάντες ὑμῖν ἁμαρτάνειν. ἐγὼ δέ, ὅτι μέν
  ποτ᾿ ἐξῆν τῇ πόλει καὶ τὰ αὑτῆς ἔχειν ἀσφαλῶς καὶ Φίλιππον
  τιμωρήσασθαι, καὶ μάλ᾿ ἀκριβῶς οἶδα· ἐπ᾿ ἐμοῦ γάρ, οὐ πάλαι
  γέγονεν ταῦτ᾿ ἀμφότερα· νῦν μέντοι πέπεισμαι τοῦθ᾿ ἱκανὸν
  προλαβεῖν ἡμῖν εἶναι τὴν πρώτην, ὅπως τοὺς συμμάχους
  σώσομεν. ἐὰν γὰρ τοῦτο βεβαίως ὑπάρξῃ, τότε καὶ περὶ τοῦ
  τίνα τιμωρήσεταί τις καὶ ὃν τρόπον ἐξέσται σκοπεῖν· πρὶν δὲ
  τὴν ἀρχὴν ὀρθῶς ὑποθέσθαι, μάταιον ἡγοῦμαι περὶ τῆς
  τελευτῆς ὁντινοῦν ποιεῖσθαι λόγον.

  Δημοσθένους, Γ´ ᾿Ολυνθιακὸς

Georgian:

  From a Unicode conference invitation:

  გთხოვთ ახლავე გაიაროთ რეგისტრაცია Unicode-ის მეათე საერთაშორისო
  კონფერენციაზე დასასწრებად, რომელიც გაიმართება 10-12 მარტს,
  ქ. მაინცში, გერმანიაში. კონფერენცია შეჰკრებს ერთად მსოფლიოს
  ექსპერტებს ისეთ დარგებში როგორიცაა ინტერნეტი და Unicode-ი,
  ინტერნაციონალიზაცია და ლოკალიზაცია, Unicode-ის გამოყენება
  ოპერაციულ სისტემებსა, და გამოყენებით პროგრამებში, შრიფტებში,
  ტექსტების დამუშავებასა და მრავალენოვან კომპიუტერულ სისტემებში.

Russian:

  From a Unicode conference invitation:

  Зарегистрируйтесь сейчас на Десятую Международную Конференцию по
  Unicode, которая состоится 10-12 марта 1997 года в Майнце в Германии.
  Конференция соберет широкий круг экспертов по  вопросам глобального
  Интернета и Unicode, локализации и интернационализации, воплощению и
  применению Unicode в различных операционных системах и программных
  приложениях, шрифтах, верстке и многоязычных компьютерных системах.

Thai (UCS Level 2):

  Excerpt from a poetry on The Romance of The Three Kingdoms (a Chinese
  classic 'San Gua'):

  [----------------------------|------------------------]
    ๏ แผ่นดินฮั่นเสื่อมโทรมแสนสังเวช  พระปกเกศกองบู๊กู้ขึ้นใหม่
  สิบสองกษัตริย์ก่อนหน้าแลถัดไป       สององค์ไซร้โง่เขลาเบาปัญญา
    ทรงนับถือขันทีเป็นที่พึ่ง           บ้านเมืองจึงวิปริตเป็นนักหนา
  โฮจิ๋นเรียกทัพทั่วหัวเมืองมา         หมายจะฆ่ามดชั่วตัวสำคัญ
    เหมือนขับไสไล่เสือจากเคหา      รับหมาป่าเข้ามาเลยอาสัญ
  ฝ่ายอ้องอุ้นยุแยกให้แตกกัน          ใช้สาวนั้นเป็นชนวนชื่นชวนใจ
    พลันลิฉุยกุยกีกลับก่อเหตุ          ช่างอาเพศจริงหนาฟ้าร้องไห้
  ต้องรบราฆ่าฟันจนบรรลัย           ฤๅหาใครค้ำชูกู้บรรลังก์ ฯ

  (The above is a two-column text. If combining characters are handled
  correctly, the lines of the second column should be aligned with the
  | character above.)

Ethiopian:

  Proverbs in the Amharic language:

  ሰማይ አይታረስ ንጉሥ አይከሰስ።
  ብላ ካለኝ እንደአባቴ በቆመጠኝ።
  ጌጥ ያለቤቱ ቁምጥና ነው።
  ደሀ በሕልሙ ቅቤ ባይጠጣ ንጣት በገደለው።
  የአፍ ወለምታ በቅቤ አይታሽም።
  አይጥ በበላ ዳዋ ተመታ።
  ሲተረጉሙ ይደረግሙ።
  ቀስ በቀስ፥ ዕንቁላል በእግሩ ይሄዳል።
  ድር ቢያብር አንበሳ ያስር።
  ሰው እንደቤቱ እንጅ እንደ ጉረቤቱ አይተዳደርም።
  እግዜር የከፈተውን ጉሮሮ ሳይዘጋው አይድርም።
  የጎረቤት ሌባ፥ ቢያዩት ይስቅ ባያዩት ያጠልቅ።
  ሥራ ከመፍታት ልጄን ላፋታት።
  ዓባይ ማደሪያ የለው፥ ግንድ ይዞ ይዞራል።
  የእስላም አገሩ መካ የአሞራ አገሩ ዋርካ።
  ተንጋሎ ቢተፉ ተመልሶ ባፉ።
  ወዳጅህ ማር ቢሆን ጨርስህ አትላሰው።
  እግርህን በፍራሽህ ልክ ዘርጋ።

Runes:

  ᚻᛖ ᚳᚹᚫᚦ ᚦᚫᛏ ᚻᛖ ᛒᚢᛞᛖ ᚩᚾ ᚦᚫᛗ ᛚᚪᚾᛞᛖ ᚾᚩᚱᚦᚹᛖᚪᚱᛞᚢᛗ ᚹᛁᚦ ᚦᚪ ᚹᛖᛥᚫ

  (Old English, which transcribed into Latin reads 'He cwaeth that he
  bude thaem lande northweardum with tha Westsae.' and means 'He said
  that he lived in the northern land near the Western Sea.')

Braille:

  ⡌⠁⠧⠑ ⠼⠁⠒  ⡍⠜⠇⠑⠹⠰⠎ ⡣⠕⠌

  ⡍⠜⠇⠑⠹ ⠺⠁⠎ ⠙⠑⠁⠙⠒ ⠞⠕ ⠃⠑⠛⠔ ⠺⠊⠹⠲ ⡹⠻⠑ ⠊⠎ ⠝⠕ ⠙⠳⠃⠞
  ⠱⠁⠞⠑⠧⠻ ⠁⠃⠳⠞ ⠹⠁⠞⠲ ⡹⠑ ⠗⠑⠛⠊⠌⠻ ⠕⠋ ⠙⠊⠎ ⠃⠥⠗⠊⠁⠇ ⠺⠁⠎
  ⠎⠊⠛⠝⠫ ⠃⠹ ⠹⠑ ⠊⠇⠻⠛⠹⠍⠁⠝⠂ ⠹⠑ ⠊⠇⠻⠅⠂ ⠹⠑ ⠥⠝⠙⠻⠞⠁⠅⠻⠂
  ⠁⠝⠙ ⠹⠑ ⠡⠊⠑⠋ ⠍⠳⠗⠝⠻⠲ ⡎⠊⠗⠕⠕⠛⠑ ⠎⠊⠛⠝⠫ ⠊⠞⠲ ⡁⠝⠙
  ⡎⠊⠗⠕⠕⠛⠑⠰⠎ ⠝⠁⠍⠑ ⠺⠁⠎ ⠛⠕⠕⠙ ⠥⠏⠕⠝ ⠰⡡⠁⠝⠛⠑⠂ ⠋⠕⠗ ⠁⠝⠹⠹⠔⠛ ⠙⠑
  ⠡⠕⠎⠑ ⠞⠕ ⠏⠥⠞ ⠙⠊⠎ ⠙⠁⠝⠙ ⠞⠕⠲

  ⡕⠇⠙ ⡍⠜⠇⠑⠹ ⠺⠁⠎ ⠁⠎ ⠙⠑⠁⠙ ⠁⠎ ⠁ ⠙⠕⠕⠗⠤⠝⠁⠊⠇⠲

  ⡍⠔⠙⠖ ⡊ ⠙⠕⠝⠰⠞ ⠍⠑⠁⠝ ⠞⠕ ⠎⠁⠹ ⠹⠁⠞ ⡊ ⠅⠝⠪⠂ ⠕⠋ ⠍⠹
  ⠪⠝ ⠅⠝⠪⠇⠫⠛⠑⠂ ⠱⠁⠞ ⠹⠻⠑ ⠊⠎ ⠏⠜⠞⠊⠊⠥⠇⠜⠇⠹ ⠙⠑⠁⠙ ⠁⠃⠳⠞
  ⠁ ⠙⠕⠕⠗⠤⠝⠁⠊⠇⠲ ⡊ ⠍⠊⠣⠞ ⠙⠁⠧⠑ ⠃⠑⠲ ⠔⠊⠇⠔⠫⠂ ⠍⠹⠎⠑⠇⠋⠂ ⠞⠕
  ⠗⠑⠛⠜⠙ ⠁ ⠊⠕⠋⠋⠔⠤⠝⠁⠊⠇ ⠁⠎ ⠹⠑ ⠙⠑⠁⠙⠑⠌ ⠏⠊⠑⠊⠑ ⠕⠋ ⠊⠗⠕⠝⠍⠕⠝⠛⠻⠹
  ⠔ ⠹⠑ ⠞⠗⠁⠙⠑⠲ ⡃⠥⠞ ⠹⠑ ⠺⠊⠎⠙⠕⠍ ⠕⠋ ⠳⠗ ⠁⠝⠊⠑⠌⠕⠗⠎
  ⠊⠎ ⠔ ⠹⠑ ⠎⠊⠍⠊⠇⠑⠆ ⠁⠝⠙ ⠍⠹ ⠥⠝⠙⠁⠇⠇⠪⠫ ⠙⠁⠝⠙⠎
  ⠩⠁⠇⠇ ⠝⠕⠞ ⠙⠊⠌⠥⠗⠃ ⠊⠞⠂ ⠕⠗ ⠹⠑ ⡊⠳⠝⠞⠗⠹⠰⠎ ⠙⠕⠝⠑ ⠋⠕⠗⠲ ⡹⠳
  ⠺⠊⠇⠇ ⠹⠻⠑⠋⠕⠗⠑ ⠏⠻⠍⠊⠞ ⠍⠑ ⠞⠕ ⠗⠑⠏⠑⠁⠞⠂ ⠑⠍⠏⠙⠁⠞⠊⠊⠁⠇⠇⠹⠂ ⠹⠁⠞
  ⡍⠜⠇⠑⠹ ⠺⠁⠎ ⠁⠎ ⠙⠑⠁⠙ ⠁⠎ ⠁ ⠙⠕⠕⠗⠤⠝⠁⠊⠇⠲

  (The first couple of paragraphs of "A Christmas Carol" by Dickens)

Compact font selection example text:

  ABCDEFGHIJKLMNOPQRSTUVWXYZ /0123456789
  abcdefghijklmnopqrstuvwxyz £©µÀÆÖÞßéöÿ
  –—‘“”„†•…‰™œŠŸž€ ΑΒΓΔΩαβγδω АБВГДабвгд
  ∀∂∈ℝ∧∪≡∞ ↑↗↨↻⇣ ┐┼╔╘░►☺♀ ﬁ�⑀₂ἠḂӥẄɐː⍎אԱა

Greetings in various languages:

  Hello world, Καλημέρα κόσμε, コンニチハ

Box drawing alignment tests:                                          █
                                                                      ▉
  ╔══╦══╗  ┌──┬──┐  ╭──┬──╮  ╭──┬──╮  ┏━━┳━━┓  ┎┒┏┑   ╷  ╻ ┏┯┓ ┌┰┐    ▊ ╱╲╱╲╳╳╳
  ║┌─╨─┐║  │╔═╧═╗│  │╒═╪═╕│  │╓─╁─╖│  ┃┌─╂─┐┃  ┗╃╄┙  ╶┼╴╺╋╸┠┼┨ ┝╋┥    ▋ ╲╱╲╱╳╳╳
  ║│╲ ╱│║  │║   ║│  ││ │ ││  │║ ┃ ║│  ┃│ ╿ │┃  ┍╅╆┓   ╵  ╹ ┗┷┛ └┸┘    ▌ ╱╲╱╲╳╳╳
  ╠╡ ╳ ╞╣  ├╢   ╟┤  ├┼─┼─┼┤  ├╫─╂─╫┤  ┣┿╾┼╼┿┫  ┕┛┖┚     ┌┄┄┐ ╎ ┏┅┅┓ ┋ ▍ ╲╱╲╱╳╳╳
  ║│╱ ╲│║  │║   ║│  ││ │ ││  │║ ┃ ║│  ┃│ ╽ │┃  ░░▒▒▓▓██ ┊  ┆ ╎ ╏  ┇ ┋ ▎
  ║└─╥─┘║  │╚═╤═╝│  │╘═╪═╛│  │╙─╀─╜│  ┃└─╂─┘┃  ░░▒▒▓▓██ ┊  ┆ ╎ ╏  ┇ ┋ ▏
  ╚══╩══╝  └──┴──┘  ╰──┴──╯  ╰──┴──╯  ┗━━┻━━┛           └╌╌┘ ╎ ┗╍╍┛ ┋  ▁▂▃▄▅▆▇█

"""


class FSTestCases(object):
    """Basic FS tests."""

    def make_fs(self):
        raise NotImplementedError('implement me')

    def destroy_fs(self, fs):
        fs.close()

    def setUp(self):
        self.fs = self.make_fs()

    def tearDown(self):
        self.destroy_fs(self.fs)
        del self.fs

    def assert_exists(self, path):
        """Assert a path exists."""
        self.assertTrue(self.fs.exists(path))

    def assert_not_exists(self, path):
        """Assert a path does not exist."""
        self.assertFalse(self.fs.exists(path))

    def assert_isfile(self, path):
        """Assert a path is a file."""
        self.assertTrue(self.fs.isfile(path))

    def assert_isdir(self, path):
        """Assert a path is a directory."""
        self.assertTrue(self.fs.isdir(path))

    def assert_bytes(self, path, contents):
        """Assert a file contains the given bytes."""
        assert isinstance(contents, bytes)
        with self.fs.open(path, 'rb') as f:
            data = f.read()
        self.assertEqual(data, contents)
        self.assertIsInstance(data, bytes)

    def assert_text(self, path, contents):
        """Assert a file contains the given text."""
        assert isinstance(contents, text_type)
        with self.fs.open(path, 'rt') as f:
            data = f.read()
        self.assertEqual(data, contents)
        self.assertIsInstance(data, text_type)

    def test_basic(self):
        # Check str and repr don't break
        repr(self.fs)
        self.assertIsInstance(six.text_type(self.fs), six.text_type)

    def test_getmeta(self):
        # Get he meta dict
        meta = self.fs.getmeta()

        # Check default namespace
        self.assertEqual(meta, self.fs.getmeta(namespace="standard"))

        # Must be a dict
        self.assertTrue(isinstance(meta, dict))

        no_meta = self.fs.getmeta('__nosuchnamespace__')
        self.assertIsInstance(no_meta, dict)
        self.assertFalse(no_meta)

    def test_isfile(self):
        self.assertFalse(self.fs.isfile('foo.txt'))
        self.fs.create('foo.txt')
        self.assertTrue(self.fs.isfile('foo.txt'))
        self.fs.makedir('bar')
        self.assertFalse(self.fs.isfile('bar'))

    def test_isdir(self):
        self.assertFalse(self.fs.isdir('foo'))
        self.fs.create('bar')
        self.fs.makedir('foo')
        self.assertTrue(self.fs.isdir('foo'))
        self.assertFalse(self.fs.isdir('bar'))

    def test_getsize(self):
        self.fs.setbytes('empty', b'')
        self.fs.setbytes('one', b'a')
        self.fs.setbytes('onethousand', ('b' * 1000).encode('ascii'))
        self.assertEqual(self.fs.getsize('empty'), 0)
        self.assertEqual(self.fs.getsize('one'), 1)
        self.assertEqual(self.fs.getsize('onethousand'), 1000)
        with self.assertRaises(errors.ResourceNotFound):
            self.fs.getsize('doesnotexist')

    def test_getsyspath(self):
        self.fs.create('foo')
        try:
            self.fs.getsyspath('foo')
        except errors.NoSysPath:
            self.assertFalse(self.fs.hassyspath('foo'))
        else:
            self.assertTrue(self.fs.hassyspath('foo'))

    def test_geturl(self):
        self.fs.create('foo')
        try:
            self.fs.geturl('foo')
        except errors.NoURL:
            self.assertFalse(self.fs.hasurl('foo'))
        else:
            self.assertTrue(self.fs.hasurl('foo'))

    def test_invalid_chars(self):
        """Test invalid path method."""
        with self.assertRaises(errors.InvalidCharsInPath):
            self.fs.open('invalid\0file', 'wb')

        with self.assertRaises(errors.InvalidCharsInPath):
            self.fs.validatepath('invalid\0file')

    def test_getinfo(self):
        # Test special case of root directory
        # Root directory has a name of ''
        root_info = self.fs.getinfo('/')
        self.assertEqual(root_info.name, '')
        self.assertTrue(root_info.is_dir)

        # Make a file of known size
        self.fs.setbytes('foo', b'bar')
        self.fs.makedir('dir')

        # Check basic namespace
        info = self.fs.getinfo('foo').raw
        self.assertEqual(info['basic']['name'], 'foo')
        self.assertFalse(info['basic']['is_dir'])

        # Check basic namespace dir
        info = self.fs.getinfo('dir').raw
        self.assertEqual(info['basic']['name'], 'dir')
        self.assertTrue(info['basic']['is_dir'])

        # Get the info
        info = self.fs.getinfo('foo', 'details').raw
        self.assertIsInstance(info, dict)
        self.assertEqual(info['details']['size'], 3)
        self.assertEqual(info['details']['type'], int(ResourceType.file))

        # Raw info should be serializable
        try:
            json.dumps(info)
        except:
            assert False, "info should be JSON serializable"

        # Non existant namespace is not an error
        no_info = self.fs.getinfo('foo', '__nosuchnamespace__').raw
        self.assertIsInstance(no_info, dict)
        self.assertEqual(
            no_info,
            {'basic': {'name': 'foo', 'is_dir': False}}
        )

        # Check a number of standard namespaces
        # FS objects may not support all these, but we can at least
        # invoke the code
        self.fs.getinfo('foo', 'access', 'stat', 'details')

    def test_exists(self):
        """Test exists method."""
        # Check root directory always exists
        self.assertTrue(self.fs.exists('/'))
        self.assertTrue(self.fs.exists(''))

        # Check files don't exist
        self.assertFalse(self.fs.exists('foo'))
        self.assertFalse(self.fs.exists('foo/bar'))
        self.assertFalse(self.fs.exists('foo/bar/baz'))
        self.assertFalse(self.fs.exists('egg'))

        # make some files and directories
        self.fs.makedirs('foo/bar')
        self.fs.setbytes('foo/bar/baz', b'test')

        # Check files exists
        self.assertTrue(self.fs.exists('foo'))
        self.assertTrue(self.fs.exists('foo/bar'))
        self.assertTrue(self.fs.exists('foo/bar/baz'))
        self.assertFalse(self.fs.exists('egg'))

        self.assert_exists('foo')
        self.assert_exists('foo/bar')
        self.assert_exists('foo/bar/baz')
        self.assert_not_exists('egg')

        # Delete a file
        self.fs.remove('foo/bar/baz')
        # Check it no longer exists
        self.assert_not_exists('foo/bar/baz')
        self.assertFalse(self.fs.exists('foo/bar/baz'))
        self.assert_not_exists('foo/bar/baz')

        # Check root directory always exists
        self.assertTrue(self.fs.exists('/'))
        self.assertTrue(self.fs.exists(''))

    def test_listdir(self):
        # Check listing directory that doesn't exist
        with self.assertRaises(errors.ResourceNotFound):
            self.fs.listdir('foobar')

        # Check aliases for root
        self.assertEqual(self.fs.listdir('/'), [])
        self.assertEqual(self.fs.listdir('.'), [])
        self.assertEqual(self.fs.listdir('./'), [])

        # Make a few files
        self.fs.setbytes('foo', b'egg')
        self.fs.setbytes('bar', b'egg')
        self.fs.setbytes('baz', b'egg')

        # Check list works
        six.assertCountEqual(self,
                             self.fs.listdir('/'),
                             ['foo', 'bar', 'baz'])
        six.assertCountEqual(self,
                             self.fs.listdir('.'),
                             ['foo', 'bar', 'baz'])
        six.assertCountEqual(self,
                             self.fs.listdir('./'),
                             ['foo', 'bar', 'baz'])

        # Check paths are unicode strings
        for name in self.fs.listdir('/'):
            self.assertIsInstance(name, text_type)

        # Create a subdirectory
        self.fs.makedir('dir')

        # Should start empty
        self.assertEqual(self.fs.listdir('/dir'), [])

        # Write some files
        self.fs.setbytes('dir/foofoo', b'egg')
        self.fs.setbytes('dir/barbar', b'egg')

        # Check listing subdirectory
        six.assertCountEqual(self,
                             self.fs.listdir('dir'),
                             ['foofoo', 'barbar'])
        # Make sure they are unicode stringd
        for name in self.fs.listdir('dir'):
            self.assertIsInstance(name, text_type)

    def test_move(self):
        # Make a file
        self.fs.setbytes('foo', b'egg')
        self.assert_isfile('foo')

        # Move it
        self.fs.move('foo', 'bar')

        # Check it has gone from original location
        self.assert_not_exists('foo')

        # Check it exists in the new location, and contents match
        self.assert_exists('bar')
        self.assert_bytes('bar', b'egg')

        # Check moving to existing file fails
        self.fs.setbytes('foo2', b'eggegg')
        with self.assertRaises(errors.DestinationExists):
            self.fs.move('foo2', 'bar')

        # Check move with overwrite=True
        self.fs.move('foo2', 'bar', overwrite=True)
        self.assert_not_exists('foo2')

        # Check moving to a non-existant directory
        with self.assertRaises(errors.ResourceNotFound):
            self.fs.move('bar', 'egg/bar')

        # Check moving between different directories
        self.fs.makedir('baz')
        self.fs.setbytes('baz/bazbaz', b'bazbaz')
        self.fs.makedir('baz2')
        self.fs.move('baz/bazbaz', 'baz2/bazbaz')
        self.assert_not_exists('baz/bazbaz')
        self.assert_bytes('baz2/bazbaz', b'bazbaz')

    def test_makedir(self):
        # Check edge case of root
        with self.assertRaises(errors.DirectoryExists):
            self.fs.makedir('/')

        # Making root is a null op with recreate
        slash_fs = self.fs.makedir('/', recreate=True)
        self.assertIsInstance(slash_fs, SubFS)
        self.assertEqual(self.fs.listdir('/'), [])

        self.assert_not_exists('foo')
        self.fs.makedir('foo')
        self.assert_isdir('foo')
        self.assertEqual(self.fs.gettype('foo'),
                         ResourceType.directory)
        self.fs.setbytes('foo/bar.txt', b'egg')
        self.assert_bytes('foo/bar.txt', b'egg')

        with self.assertRaises(errors.DirectoryExists):
            self.fs.makedir('foo')

        with self.assertRaises(errors.ParentDirectoryMissing):
            self.fs.makedir('/foo/bar/baz')

        self.fs.makedir('/foo/bar')
        self.fs.makedir('/foo/bar/baz')

        with self.assertRaises(errors.DirectoryExists):
            self.fs.makedir('foo/bar/baz')

    def test_makedirs(self):
        self.assertFalse(self.fs.exists('foo'))
        self.fs.makedirs('foo')
        self.assertEqual(self.fs.gettype('foo'),
                         ResourceType.directory)

        self.fs.makedirs('foo/bar/baz')
        self.assertTrue(self.fs.isdir('foo/bar'))
        self.assertTrue(self.fs.isdir('foo/bar/baz'))

        with self.assertRaises(errors.DirectoryExists):
            self.fs.makedirs('foo/bar/baz')

        self.fs.makedirs('foo/bar/baz', recreate=True)

        self.fs.setbytes('foo.bin', b'test')
        with self.assertRaises(errors.DirectoryExpected):
            self.fs.makedirs('foo.bin/bar')

        with self.assertRaises(errors.DirectoryExpected):
            self.fs.makedirs('foo.bin/bar/baz/egg')

    def test_open(self):
        # Open a file that doesn't exist
        with self.assertRaises(errors.ResourceNotFound):
            self.fs.open('doesnotexist', 'r')

        self.fs.makedir('foo')

        # Create a new text file
        text = 'Hello, World'

        with self.fs.open('foo/hello', 'wt') as f:
            f.write(text)

        # Read it back
        with self.fs.open('foo/hello', 'rt') as f:
            hello = f.read()
        self.assertEqual(hello, text)
        self.assert_text('foo/hello', text)

        # Test overwrite
        text = 'Goodbye, World'
        with self.fs.open('foo/hello', 'wt') as f:
            f.write(text)
        self.assert_text('foo/hello', text)

        # Open from missing dir
        with self.assertRaises(errors.ResourceNotFound):
            self.fs.open('/foo/bar/test.txt')

    def test_openbin(self):
        # Write a binary file
        with self.fs.openbin('file.bin', 'wb') as write_file:
            write_file.write(b'\0\1\2')
        # Read a binary file
        with self.fs.openbin('file.bin', 'rb') as read_file:
            data = read_file.read()
        self.assertEqual(data, b'\0\1\2')

        # Check disallow text mode
        with self.assertRaises(ValueError):
            with self.fs.openbin('file.bin', 'rt') as read_file:
                pass

        # Check errors
        with self.assertRaises(errors.ResourceNotFound):
            self.fs.openbin('foo.bin')

        # Open from missing dir
        with self.assertRaises(errors.ResourceNotFound):
            self.fs.openbin('/foo/bar/test.txt')

    def test_opendir(self):
        self.fs.makedir('foo')
        self.fs.setbytes('foo/bar', b'barbar')
        self.fs.setbytes('foo/egg', b'eggegg')

        # Open a sub directory
        with self.fs.opendir('foo') as foo_fs:
            six.assertCountEqual(self, foo_fs.listdir('/'), ['bar', 'egg'])
            self.assertTrue(foo_fs.isfile('bar'))
            self.assertTrue(foo_fs.isfile('egg'))
            self.assertEqual(foo_fs.getbytes('bar'), b'barbar')
            self.assertEqual(foo_fs.getbytes('egg'), b'eggegg')

        # Attempt to open a non-existent directory
        with self.assertRaises(errors.ResourceNotFound):
            self.fs.opendir('egg')

        # Check error when doing opendir on a non dir
        with self.assertRaises(errors.ResourceInvalid):
            self.fs.opendir('foo/egg')

        # These should work, and will essentially return a 'clone' of sorts
        self.fs.opendir('')
        self.fs.opendir('/')

    def test_remove(self):

        self.fs.setbytes('foo1', b'test1')
        self.fs.setbytes('foo2', b'test2')
        self.fs.setbytes('foo3', b'test3')

        self.assert_isfile('foo1')
        self.assert_isfile('foo2')
        self.assert_isfile('foo3')

        self.fs.remove('foo2')

        self.assert_isfile('foo1')
        self.assert_not_exists('foo2')
        self.assert_isfile('foo3')

        with self.assertRaises(errors.ResourceNotFound):
            self.fs.remove('bar')

        self.fs.makedir('dir')
        with self.assertRaises(errors.ResourceInvalid):
            self.fs.remove('dir')

    def test_removedir(self):

        self.fs.makedirs('foo/bar/baz')
        self.assertTrue(self.fs.exists('foo/bar/baz'))
        self.fs.removedir('foo/bar/baz')
        self.assertFalse(self.fs.exists('foo/bar/baz'))
        self.assertTrue(self.fs.isdir('foo/bar'))

        with self.assertRaises(errors.ResourceNotFound):
            self.fs.removedir('nodir')

        # Test force removal
        self.fs.makedirs('foo/bar/baz')
        self.fs.setbytes('foo/egg', b'test')

        with self.assertRaises(errors.DirectoryExpected):
            self.fs.removedir('foo/egg')

        with self.assertRaises(errors.DirectoryNotEmpty):
            self.fs.removedir('foo/bar')

    def test_removetree(self):
        self.fs.makedirs('foo/bar/baz')
        self.fs.create('foo/egg.txt')
        self.fs.create('foo/bar/egg.bin')

        self.assert_exists('foo/egg.txt')
        self.assert_exists('foo/bar/egg.bin')

        self.fs.removetree('foo')
        self.assert_not_exists('foo')

    def test_setinfo(self):
        self.fs.create('birthday.txt')
        now = math.floor(time.time())

        change_info = {
            'details':
            {
                'accessed': now + 60,
                'modified': now + 60 * 60
            }
        }
        self.fs.setinfo('birthday.txt', change_info)
        new_info = self.fs.getinfo(
            'birthday.txt',
            'details'
        ).raw
        self.assertEqual(new_info['details']['accessed'], now + 60)
        self.assertEqual(new_info['details']['modified'], now + 60 * 60)

        with self.assertRaises(errors.ResourceNotFound):
            self.fs.setinfo('nothing', {})

    def test_settimes(self):
        self.fs.create('birthday.txt')
        self.fs.settimes(
            'birthday.txt',
            accessed=datetime(2016, 7, 5),
        )
        info = self.fs.getinfo('birthday.txt', 'details')
        self.assertEqual(info.accessed, datetime(2016, 7, 5, tzinfo=pytz.UTC))
        self.assertEqual(info.modified, datetime(2016, 7, 5, tzinfo=pytz.UTC))

    def test_touch(self):
        self.fs.touch('new.txt')
        self.assert_isfile('new.txt')
        self.fs.settimes('new.txt', datetime(2016, 7, 5))
        info = self.fs.getinfo('new.txt', 'details')
        self.assertEqual(info.accessed, datetime(2016, 7, 5, tzinfo=pytz.UTC))
        now = time.time()
        self.fs.touch('new.txt')
        accessed = self.fs.getinfo('new.txt', 'details').raw['details']['accessed']
        self.assertTrue(accessed - now < 5)

    def test_close(self):
        self.assertFalse(self.fs.isclosed())
        self.fs.close()
        self.assertTrue(self.fs.isclosed())
        # Check second close call is a no-op
        self.fs.close()
        self.assertTrue(self.fs.isclosed())

        # Check further operations raise a FilesystemClosed exception
        with self.assertRaises(errors.FilesystemClosed):
            self.fs.openbin('test.bin')

    def test_copy(self):
        # Test copy to new path
        self.fs.setbytes('foo', b'test')
        self.fs.copy('foo', 'bar')
        self.assert_bytes('bar', b'test')

        # Test copy over existing path
        self.fs.setbytes('baz', b'truncateme')
        self.fs.copy('foo', 'baz')
        self.assert_bytes('foo', b'test')

    def test_create(self):
        # Test create new file
        self.assertFalse(self.fs.exists('foo'))
        self.fs.create('foo')
        self.assertTrue(self.fs.exists('foo'))
        self.assertEqual(self.fs.gettype('foo'), ResourceType.file)
        self.assertEqual(self.fs.getsize('foo'), 0)

        # Test wipe existing file
        self.fs.setbytes('foo', b'bar')
        self.assertEqual(self.fs.getsize('foo'), 3)
        self.fs.create('foo', wipe=True)
        self.assertEqual(self.fs.getsize('foo'), 0)

        # Test create with existing file, and not wipe
        self.fs.setbytes('foo', b'bar')
        self.assertEqual(self.fs.getsize('foo'), 3)
        self.fs.create('foo', wipe=False)
        self.assertEqual(self.fs.getsize('foo'), 3)

    def test_desc(self):
        # Describe a file
        self.fs.create('foo')
        description = self.fs.desc('foo')
        self.assertIsInstance(description, text_type)

        # Describe a dir
        self.fs.makedir('dir')
        self.fs.desc('dir')

        # Special cases that may hide bugs
        self.fs.desc('/')
        self.fs.desc('')

        with self.assertRaises(errors.ResourceNotFound):
            self.fs.desc('bar')

    def test_scandir(self):
        # Check exception for scanning dir that doesn't exist
        with self.assertRaises(errors.ResourceNotFound):
            for info in self.fs.scandir('/foobar'):
                pass

        # Check scandir returns an iterable
        iter_scandir = self.fs.scandir('/')
        self.assertTrue(isinstance(iter_scandir, collections.Iterable))
        self.assertEqual(list(iter_scandir), [])

        # Check scanning
        self.fs.create('foo')
        self.fs.create('bar')
        self.fs.makedir('dir')
        iter_scandir = self.fs.scandir('/')
        self.assertTrue(isinstance(iter_scandir, collections.Iterable))

        scandir = sorted(
            [r.raw for r in iter_scandir],
            key=lambda info: info['basic']['name']
        )

        self.assertEqual(scandir, [
            {'basic': {'name': 'bar', 'is_dir': False}},
            {'basic': {'name': 'dir', 'is_dir': True}},
            {'basic': {'name': 'foo', 'is_dir': False}},
        ])

        # Hard to test optional namespaces, but at least run the code
        list(self.fs.scandir('/', namespaces=['details', 'stat', 'access']))

    def test_filterdir(self):
        self.assertEqual(
            list(self.fs.filterdir('/', wildcards=['*.py'])),
            []
        )

        self.fs.makedir('bar')
        self.fs.create('foo.txt')
        self.fs.create('foo.py')
        self.fs.create('foo.pyc')

        # Check filtering by wildcard
        dir_list = [info.name for info in self.fs.filterdir('/', wildcards=['*.py'])]
        self.assertEqual(set(dir_list), {'bar', 'foo.py'})

        # Check filtering by miltiple wildcard
        dir_list = [info.name for info in self.fs.filterdir('/', wildcards=['*.py', '*.pyc'])]
        self.assertEqual(set(dir_list), {'bar', 'foo.py', 'foo.pyc'})

        # Check excluding dirs
        dir_list = [info.name for info in self.fs.filterdir('/', exclude_dirs=True, wildcards=['*.py', '*.pyc'])]
        self.assertEqual(set(dir_list), {'foo.py', 'foo.pyc'})

        # Check excluding files
        dir_list = [info.name for info in self.fs.filterdir('/', exclude_files=True)]
        self.assertEqual(set(dir_list), {'bar'})

        # Check wildcards must be a list
        with self.assertRaises(ValueError):
            dir_list = [info.name for info in self.fs.filterdir('/', wildcards="*.py")]

        self.fs.makedir('baz')
        dir_list = [info.name for info in self.fs.filterdir('/', exclude_files=True, dir_wildcards=['??z'])]
        self.assertEqual(set(dir_list), {'baz'})

        with self.assertRaises(ValueError):
            dir_list = [info.name for info in self.fs.filterdir('/', exclude_files=True, dir_wildcards="*.py")]

    def test_getbytes(self):
        """Test getbytes method."""
        all_bytes = b''.join(six.int2byte(n) for n in range(256))
        with self.fs.open('foo', 'wb') as f:
            f.write(all_bytes)
        self.assertEqual(self.fs.getbytes('foo'), all_bytes)
        _all_bytes = self.fs.getbytes('foo')
        self.assertIsInstance(_all_bytes, bytes)
        self.assertEqual(_all_bytes, all_bytes)

    def test_isempty(self):
        self.assertTrue(self.fs.isempty('/'))
        self.fs.makedir('foo')
        self.assertFalse(self.fs.isempty('/'))
        self.assertTrue(self.fs.isempty('/foo'))
        self.fs.create('foo/bar.txt')
        self.assertFalse(self.fs.isempty('/foo'))
        self.fs.remove('foo/bar.txt')
        self.assertTrue(self.fs.isempty('/foo'))

    def test_setbytes(self):
        all_bytes = b''.join(six.int2byte(n) for n in range(256))
        self.fs.setbytes('foo', all_bytes)
        with self.fs.open('foo', 'rb') as f:
            _bytes = f.read()
        self.assertIsInstance(_bytes, bytes)
        self.assertEqual(_bytes, all_bytes)
        self.assert_bytes('foo', all_bytes)
        with self.assertRaises(ValueError):
            self.fs.setbytes('notbytes', 'unicode')

    def test_gettext(self):
        self.fs.makedir('foo')
        with self.fs.open('foo/unicode.txt', 'wt') as f:
            f.write(UNICODE_TEXT)
        text = self.fs.gettext('foo/unicode.txt')
        self.assertIsInstance(text, text_type)
        self.assertEqual(text, UNICODE_TEXT)
        self.assert_text('foo/unicode.txt', UNICODE_TEXT)

    def test_settext(self):
        """Test settext method."""
        self.fs.settext('foo', 'bar')
        with self.fs.open('foo', 'rt') as f:
            foo = f.read()
        self.assertEqual(foo, 'bar')
        self.assertIsInstance(foo, text_type)
        with self.assertRaises(ValueError):
            self.fs.settext('nottext', b'bytes')

    def test_setfile(self):
        bytes_file = io.BytesIO(b'bar')
        self.fs.setfile('foo', bytes_file)
        with self.fs.open('foo', 'rb') as f:
            data = f.read()
        self.assertEqual(data, b'bar')

    def test_bin_files(self):
        """Check binary files."""
        with self.fs.openbin('foo1', 'wb') as f:
            text_type(f)
            repr(f)
            f.write(b'a')
            f.write(b'b')
            f.write(b'c')
        self.assert_bytes('foo1', b'abc')

        # Test writelines
        with self.fs.openbin('foo2', 'wb') as f:
            f.writelines([b'hello\n', b'world'])
        self.assert_bytes('foo2', b'hello\nworld')

        # Test readline
        with self.fs.openbin('foo2') as f:
            self.assertEqual(f.readline(), b'hello\n')
            self.assertEqual(f.readline(), b'world')

        # Test readlines
        with self.fs.openbin('foo2') as f:
            lines = f.readlines()
        self.assertEqual(lines, [b'hello\n', b'world'])
        with self.fs.openbin('foo2') as f:
            lines = list(f)
        self.assertEqual(lines, [b'hello\n', b'world'])
        with self.fs.openbin('foo2') as f:
            lines = []
            for line in f:
                lines.append(line)
        self.assertEqual(lines, [b'hello\n', b'world'])
        with self.fs.openbin('foo2') as f:
            print(repr(f))
            self.assertEqual(next(f), b'hello\n')

        # Test truncate
        with self.fs.open('foo2', 'rb+') as f:
            f.truncate(3)
        self.assertEqual(self.fs.getsize('foo2'), 3)
        self.assert_bytes('foo2', b'hel')

    def test_files(self):
        # Test multiple writes

        with self.fs.open('foo1', 'wt') as f:
            text_type(f)
            repr(f)
            f.write('a')
            f.write('b')
            f.write('c')
        self.assert_text('foo1', 'abc')

        # Test writelines
        with self.fs.open('foo2', 'wt') as f:
            f.writelines(['hello\n', 'world'])
        self.assert_text('foo2', 'hello\nworld')

        # Test readline
        with self.fs.open('foo2') as f:
            self.assertEqual(f.readline(), 'hello\n')
            self.assertEqual(f.readline(), 'world')

        # Test readlines
        with self.fs.open('foo2') as f:
            lines = f.readlines()
        self.assertEqual(lines, ['hello\n', 'world'])
        with self.fs.open('foo2') as f:
            lines = list(f)
        self.assertEqual(lines, ['hello\n', 'world'])
        with self.fs.open('foo2') as f:
            lines = []
            for line in f:
                lines.append(line)
        self.assertEqual(lines, ['hello\n', 'world'])

        # Test truncate
        with self.fs.open('foo2', 'r+') as f:
            f.truncate(3)
        self.assertEqual(self.fs.getsize('foo2'), 3)
        self.assert_text('foo2', 'hel')

        with self.fs.open('foo2', 'ab') as f:
            f.write(b'p')
        self.assert_bytes('foo2', b'help')

    def test_copy_file(self):
        """Test fs.copy.copy_file"""
        bytes_test = b'Hello, World'
        self.fs.setbytes('foo.txt', bytes_test)
        fs.copy.copy_file(self.fs, 'foo.txt', self.fs, 'bar.txt')
        self.assert_bytes('bar.txt', bytes_test)

        mem_fs = open_fs('mem://')

        fs.copy.copy_file(self.fs, 'foo.txt', mem_fs, 'bar.txt')
        self.assertEqual(mem_fs.getbytes('bar.txt'), bytes_test)

    def test_copy_structure(self):
        mem_fs = open_fs('mem://')
        self.fs.makedirs('foo/bar/baz')
        self.fs.makedir('egg')

        fs.copy.copy_structure(self.fs, mem_fs)
        expected = {
            "/egg",
            "/foo",
            "/foo/bar",
            "/foo/bar/baz",
        }
        self.assertEqual(
            set(walk.walk_dirs(mem_fs)),
            expected
        )

    def _test_copy_dir(self, protocol):
        """Test copy.copy_dir."""

        # Test copying to a another fs
        other_fs = open_fs(protocol)
        self.fs.makedirs('foo/bar/baz')
        self.fs.makedir('egg')
        self.fs.settext('top.txt', 'Hello, World')
        self.fs.settext('/foo/bar/baz/test.txt', 'Goodbye, World')

        fs.copy.copy_dir(self.fs, '/', other_fs, '/')
        expected = {
            "/egg",
            "/foo",
            "/foo/bar",
            "/foo/bar/baz",
        }
        self.assertEqual(
            set(walk.walk_dirs(other_fs)),
            expected
        )
        self.assert_text('top.txt', 'Hello, World')
        self.assert_text('/foo/bar/baz/test.txt', 'Goodbye, World')

        # Test copying a sub dir
        other_fs = open_fs('mem://')
        fs.copy.copy_dir(self.fs, '/foo', other_fs, '/')
        self.assertEqual(
            list(walk.walk_files(other_fs)),
            ['/bar/baz/test.txt']
        )

        # Test copying to a sub dir
        other_fs = open_fs(protocol)
        with self.assertRaises(fs.copy.CopyError):
            fs.copy.copy_dir(self.fs, '/foo', other_fs, '/egg')

        fs.copy.copy_dir(self.fs, '/foo', other_fs, '/egg', create=True)

        self.assertEqual(
            list(walk.walk_files(other_fs)),
            ['/egg/bar/baz/test.txt']
        )

    def _test_copy_dir_write(self, protocol):
        """Test copying to this filesystem from another."""

        other_fs = open_fs(protocol)
        other_fs.makedirs('foo/bar/baz')
        other_fs.makedir('egg')
        other_fs.settext('top.txt', 'Hello, World')
        other_fs.settext('/foo/bar/baz/test.txt', 'Goodbye, World')
        fs.copy.copy_dir(other_fs, '/', self.fs, '/')
        expected = {
            "/egg",
            "/foo",
            "/foo/bar",
            "/foo/bar/baz",
        }
        self.assertEqual(
            set(walk.walk_dirs(self.fs)),
            expected
        )
        self.assert_text('top.txt', 'Hello, World')
        self.assert_text('/foo/bar/baz/test.txt', 'Goodbye, World')

    def test_copy_dir_mem(self):
        """Test copy_dir with a mem fs."""
        self._test_copy_dir('mem://')
        self._test_copy_dir_write('mem://')

    def test_copy_dir_temp(self):
        """Test copy_dir with a temp fs."""
        self._test_copy_dir('temp://')
        self._test_copy_dir_write('temp://')

    def _test_move_dir_write(self, protocol):
        """Test moving to this filesystem from another."""
        other_fs = open_fs(protocol)
        other_fs.makedirs('foo/bar/baz')
        other_fs.makedir('egg')
        other_fs.settext('top.txt', 'Hello, World')
        other_fs.settext('/foo/bar/baz/test.txt', 'Goodbye, World')

        fs.move.move_dir(other_fs, '/', self.fs, '/')

        expected = {
            "/egg",
            "/foo",
            "/foo/bar",
            "/foo/bar/baz",
        }
        self.assertEqual(
            other_fs.listdir('/'),
            []
        )
        self.assertEqual(
            set(walk.walk_dirs(self.fs)),
            expected
        )
        self.assert_text('top.txt', 'Hello, World')
        self.assert_text('/foo/bar/baz/test.txt', 'Goodbye, World')

    def test_move_dir_mem(self):
        self._test_move_dir_write('mem://')

    def test_move_dir_temp(self):
        self._test_move_dir_write('temp://')

    def test_move_same_fs(self):
        self.fs.makedirs('foo/bar/baz')
        self.fs.makedir('egg')
        self.fs.settext('top.txt', 'Hello, World')
        self.fs.settext('/foo/bar/baz/test.txt', 'Goodbye, World')

        with self.assertRaises(fs.move.MoveError):
            fs.move.move_dir(self.fs, 'foo', self.fs, 'foo2')

        fs.move.move_dir(self.fs, 'foo', self.fs, 'foo2', create=True)

        expected = {
            "/egg",
            "/foo2",
            "/foo2/bar",
            "/foo2/bar/baz",
        }
        self.assertEqual(
            set(walk.walk_dirs(self.fs)),
            expected
        )
        self.assert_text('top.txt', 'Hello, World')
        self.assert_text('/foo2/bar/baz/test.txt', 'Goodbye, World')

    def test_move_file_same_fs(self):
        text = 'Hello, World'
        self.fs.makedir('foo').settext('test.txt', text)
        self.assert_text('foo/test.txt', text)

        fs.move.move_file(self.fs, 'foo/test.txt', self.fs, 'foo/test2.txt')
        self.assert_not_exists('foo/test.txt')
        self.assert_text('foo/test2.txt', text)

    def _test_move_file(self, protocol):
        other_fs = open_fs(protocol)

        text = 'Hello, World'
        self.fs.makedir('foo').settext('test.txt', text)
        self.assert_text('foo/test.txt', text)

        with self.assertRaises(errors.ResourceNotFound):
            fs.move.move_file(self.fs, 'foo/test.txt', other_fs, 'foo/test2.txt')

        other_fs.makedir('foo')

        fs.move.move_file(self.fs, 'foo/test.txt', other_fs, 'foo/test2.txt')

        self.assertEqual(
            other_fs.gettext('foo/test2.txt'),
            text
        )

    def test_move_file_mem(self):
        self._test_move_file('mem://')

    def test_move_file_temp(self):
        self._test_move_file('temp://')

    def test_copydir(self):
        self.fs.makedirs('foo/bar/baz/egg')
        self.fs.settext('foo/bar/foofoo.txt', 'Hello')
        self.fs.makedir('foo2')
        self.fs.copydir('foo/bar', 'foo2')
        self.assert_text('foo2/foofoo.txt', 'Hello')
        self.assert_isdir('foo2/baz/egg')
        self.assert_text('foo/bar/foofoo.txt', 'Hello')
        self.assert_isdir('foo/bar/baz/egg')

    def test_movedir(self):
        self.fs.makedirs('foo/bar/baz/egg')
        self.fs.settext('foo/bar/foofoo.txt', 'Hello')
        self.fs.makedir('foo2')
        self.fs.movedir('foo/bar', 'foo2')
        self.assert_text('foo2/foofoo.txt', 'Hello')
        self.assert_isdir('foo2/baz/egg')
        self.assert_not_exists('foo/bar/foofoo.txt')
        self.assert_not_exists('foo/bar/baz/egg')