"""Contains the Tile class that represents a 4x4 tile."""
import os.path
from dinopy import FastaReader
import sequences as seq

class Tile():
    """Represents a 4x4 tile."""

    def __init__(self, c, n, e, s, w, nw, ne, se, sw):
        """Create Tile from the 9 sequences."""
        self.c = seq.SequenceC(c)
        self.n = seq.SequenceN(n)
        self.e = seq.SequenceE(e)
        self.s = seq.SequenceS(s)
        self.w = seq.SequenceW(w)
        self.nw = seq.SequenceNW(nw)
        self.ne = seq.SequenceNE(ne)
        self.se = seq.SequenceSE(se)
        self.sw = seq.SequenceSW(sw)

    @staticmethod
    def from_file(filename):
        """Read 4x4 tile from .fasta file."""
        assert os.path.isfile(filename)

        reader = FastaReader(filename)

        for entry in reader.entries():

            name = entry.name.decode("utf-8")
            seq = entry.sequence.decode("utf-8")

            if(name == 'N'):
                n_seq = seq
            elif(name == 'E'):
                e_seq = seq
            elif(name == 'S'):
                s_seq = seq
            elif(name == 'W'):
                w_seq = seq
            elif(name == 'NE'):
                ne_seq = seq
            elif(name == 'SE'):
                se_seq = seq
            elif(name == 'SW'):
                sw_seq = seq
            elif(name == 'NW'):
                nw_seq = seq
            elif(name == 'C'):
                c_seq = seq

        return Tile(c_seq, n_seq, e_seq, s_seq, w_seq,
                    nw_seq, ne_seq, se_seq, sw_seq)

    @staticmethod
    def from_random(freq={b:1 for b in "ATGC"}):
        """
        Generate a random 4x4 tile.

        Generate a random sequence with given base frequencies.

        Args:
            length (int): lengths of the sequence
            freq (dict(char -> float)): frequencies of the bases (default all 1)

        Returns:
            Tile: random 4x4 tile
        """
        nw = seq.SequenceNW.from_random(freq)
        ne = seq.SequenceNE.from_random(freq)
        se = seq.SequenceSE.from_random(freq)
        sw = seq.SequenceSW.from_random(freq)
        c = seq.SequenceC.from_nw_ne_se_sw(nw, ne, se, sw)
        n = seq.SequenceN.from_nw_ne_random(nw, ne, freq)
        e = seq.SequenceE.from_ne_se_random(ne, se, freq)
        s = seq.SequenceS.from_se_sw_random(se, sw, freq)
        w = seq.SequenceW.from_sw_nw_random(sw, nw, freq)
        return Tile(c, n, e, s, w, nw, ne, se, sw)

    def __str__(self):
        """Get a string representation of the 4x4 tile."""
        tile_str = "C: {}\n".format(''.join(self.c))

        tile_str += "N: {}\n".format(''.join(self.n))
        tile_str += "E: {}\n".format(''.join(self.e))
        tile_str += "S: {}\n".format(''.join(self.s))
        tile_str += "W: {}\n".format(''.join(self.w))

        tile_str += "NW: {}\n".format(''.join(self.nw))
        tile_str += "NE: {}\n".format(''.join(self.ne))
        tile_str += "SE: {}\n".format(''.join(self.se))
        tile_str += "SW: {}\n".format(''.join(self.sw))
        return tile_str

    def __repr__(self):
        """Get a string representation of the 4x4 tile."""
        return str(self)
