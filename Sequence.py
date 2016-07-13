"""This module contains classes that represent sequences of a 4x4 tile."""
import random

class Sequence(list):
    """
    Represents a DNA sequence.

    Enhances String class with useful methods for sequences.
    """

    def get_part(self, part):
        """
        Get specific numbered part of sequence.

        For use in specific class (e.g. SequenceC, SequenceNE) only.
        If there is no number, use "head" and "tail".

        Args:
            part (int or string): numbered part of sequence or "head"/"tail"
        """
        assert part in self._partition.keys()
        start, end = self._partition[part]
        return Sequence(self[start:end])

    def set_part(self, part, new_seq):
        """
        Set specific numbered part of sequence.

        For use in specific class (e.g. SequenceC, SequenceNE) only.
        If there is no number, use "head" and "tail".

        Args:
            part (int or string): numbered part of sequence or "head"/"tail"
            new_seq (string): new sequence
        """
        assert part in self._partition.keys()
        start, end = self._partition[part]
        assert len(new_seq) == end-start
        self[start:end] = new_seq

    def rev_comp(self):
        """
        Calculate the reverse complement of the sequence.

        Returns:
            string: reverse complement of the sequence
        """
        complements = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
        return Sequence(map(lambda b: complements[b], self[::-1]))

    def check_q_uniqueness(self, q):
        """
        Check, if the sequence is q-unique.

        Returns a tuple (a, b) where a and b are indices of q-grams which
        violate against the conditions of q-uniqueness:
        1. Each q-gram is unique in the sequence.
        2. The reverse complement is not in the sequence.
        3. There is no reverse complement in the sequence. (a = b)
        If the sequence is q-unique, a and b are None.

        Args:
            q (int): positive number for q-uniqueness

        Returns:
            (int, int): indices of q-grams that violate agains q-uniqueness
        """
        assert type(q) is int
        assert q > 0

        qgrams = dict()
        for i in range(0, len(self)-q+1):
            qgram = self[i:i+q]
            qgram_rc = reverse_complement(qgram)
            if qgram in qgrams.keys():
                return (qgrams[qgram], i)
            qgrams[qgram] = i
            if qgram_rc in qgrams.keys():
                return (qgrams[qgram_rc], i)
            qgrams[qgram_rc] = i

        return (None, None)

    def melting_temperature(self):
        """
        Calculate melting temperature of the seqence.

        Returns the melting temperature of sequence with following formular:
        tm = 2*(#AT) + 4*(#GC)

        Returns:
            float: melting temperature of subsequence
        """
        base_count = {base:self.count(base) for base in "ATGC"}

        return 2*(base_count["A"] + base_count["T"]) + 4*(base_count["G"] + base_count["C"])

    def base_amounts_absolute(self):
        """
        Calculate the absolute amount of each base in the sequence.

        Returns:
            dict(char -> int): absolute amount of each base
        """
        return {b:self.count(b) for b in 'ATGC'}

    def base_amounts_relative(self):
        """
        Calculate the relative amount of each base in the sequence.

        Returns:
            dict(char -> float): relative amount of each base
        """
        return {b:self.count(b)/len(self) for b in 'ATGC'}

    @classmethod
    def from_random(cls, length, freqs={b:1 for b in "ATGC"}):
        """
        Generate a random sequence.

        Generate a random sequence with given base frequencies.

        Args:
            length (int): lengths of the sequence
            freq (dict(char -> float)): frequencies of the bases (default all 1)

        Returns:
            Sequence: random sequence
        """
        bounds = []
        maxbound = 0
        for base, freq in freqs.items():
            maxbound += freq
            bounds.append((base, maxbound))
        def get_base(value):
            for base, bound in bounds:
                if value < bound:
                    return base
        seq = ""
        for i in range(0, length):
            seq += get_base(random.uniform(0, maxbound))
        return cls(seq)

    def __str__(self):
        """Get string representation of sequence."""
        return ''.join(self)

    def __repr__(self):
        """Get string representation of sequence."""
        return str(self)


class SequenceC(Sequence):
    """Represents the center sequence of a 4x4 tile."""

    length = 100
    _partition = {
        "head": (None,5),
        12: (5,15),
        7: (19,30),
        9: (30,40),
        6: (44,55),
        13: (55,65),
        8: (69,80),
        11: (80,90),
        "tail": (94,None)
    }

    def get_part(self, part):
        """See Sequence.get_part."""
        # special case for 4 because end of C is inside of 4
        if 4 == part:
            return super().get_part("tail") + super().get_part("head")
        else:
            return super().get_part(part)

    @staticmethod
    def from_nw_ne_se_sw(nw, ne, se, sw):
        """
        Generate from the four outer sequences of 4x4 tile.

        Args:
            nw (SequenceNW): nw sequence of 4x4 tile
            ne (SequenceNE): nw sequence of 4x4 tile
            se (SequenceSE): nw sequence of 4x4 tile
            sw (SequenceSW): nw sequence of 4x4 tile

        Returns:
            SequenceC
        """
        assert type(nw) is SequenceNW
        assert type(ne) is SequenceNE
        assert type(se) is SequenceSE
        assert type(sw) is SequenceSW
        nw_rc = nw.rev_comp()
        ne_rc = ne.rev_comp()
        se_rc = se.rev_comp()
        sw_rc = sw.rev_comp()
        seq = ne_rc[29:34] + nw_rc[8:18] + list('TTTT')
        seq += nw_rc[18:29] + sw_rc[8:18] + list('TTTT')
        seq += sw_rc[18:29] + se_rc[13:23] + list('TTTT')
        seq += se_rc[23:34] + ne_rc[13:23] + list('TTTT')
        seq += ne_rc[23:29]
        return SequenceC(seq)


class SequenceN(Sequence):
    """Represents the northern sequence of a 4x4 tile."""

    length = 26
    _partition = {
        "tail": (None,5),
        10: (5,13),
        15: (13,21),
        "head": (21,None)
    }

    @staticmethod
    def from_nw_ne_random(nw, ne, freq={b:1 for b in "ATGC"}):
        """Generate new N-sequence from NW, NE and random head/tail."""
        n_seq = SequenceN.from_random(SequenceN.length, freq)
        n_seq.set_part(10, nw.get_part(10).rev_comp())
        n_seq.set_part(15, ne.get_part(15).rev_comp())
        return n_seq


class SequenceE(Sequence):
    """Represents the east sequence of a 4x4 tile."""

    length = 36
    _partition = {
        "tail": (None,5),
        5: (5,18),
        2: (18,31),
        "head": (31,None)
    }

    @staticmethod
    def from_ne_se_random(ne, se, freq={b:1 for b in "ATGC"}):
        """Generate new E-sequence from NE, SE and random head/tail."""
        e_seq = SequenceE.from_random(SequenceE.length, freq)
        e_seq.set_part(5, ne.get_part(5).rev_comp())
        e_seq.set_part(2, se.get_part(2).rev_comp())
        return e_seq


class SequenceS(Sequence):
    """Represents the south sequence of a 4x4 tile."""

    length = 36
    _partition = {
        "tail": (None,5),
        3: (5,18),
        1: (18,31),
        "head": (31,None)
    }

    @staticmethod
    def from_se_sw_random(se, sw, freq={b:1 for b in "ATGC"}):
        """Generate new S-sequence from SE, SW and random head/tail."""
        s_seq = SequenceS.from_random(SequenceS.length, freq)
        s_seq.set_part(3, se.get_part(3).rev_comp())
        s_seq.set_part(1, sw.get_part(1).rev_comp())
        return s_seq


class SequenceW(Sequence):
    """Represents the western sequence of a 4x4 tile."""

    length = 26
    _partition = {
        "tail": (None,5),
        16: (5,13),
        14: (13,21),
        "head": (21,None)
    }

    @staticmethod
    def from_sw_nw_random(sw, nw, freq={b:1 for b in "ATGC"}):
        """Generate new N-sequence from NW, NE and random head/tail."""
        w_seq = SequenceW.from_random(SequenceW.length, freq)
        w_seq.set_part(16, sw.get_part(16).rev_comp())
        w_seq.set_part(14, nw.get_part(14).rev_comp())
        return w_seq


class SequenceOuter(Sequence):
    """Represents an outer sequence of a 4x4 tile."""

    length = 42

    @classmethod
    def from_random(cls, freq={b:1 for b in "ATGC"}):
        """
        Generate a random sequence.

        For details see Sequence.from_random.
        """
        return cls(Sequence.from_random(cls.length, freq))


class SequenceNW(SequenceOuter):
    """Represents the northern west outer sequence of a 4x4 tile."""

    length = 37
    _partition = {
        14: (None,8),
        7: (8,19),
        12: (19,29),
        10: (29,None)
    }

class SequenceNE(SequenceOuter):
    """Represents the northern east outer sequence of a 4x4 tile."""

    length = 42
    _partition = {
        15: (None,8),
        4: (8,19),
        11: (19,29),
        5: (29,None)
    }

class SequenceSE(SequenceOuter):
    """Represents the south east outer sequence of a 4x4 tile."""

    length = 47
    _partition = {
        2: (None,13),
        8: (13,24),
        13: (24,34),
        3: (34,None)
    }


class SequenceSW(SequenceOuter):
    """Represents the south west outer sequence of a 4x4 tile."""

    length = 42
    _partition = {
        1: (None,13),
        6: (13,24),
        9: (24,34),
        16: (34,None)
    }
