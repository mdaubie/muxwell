from __future__ import annotations

import pytest

from muxwell.filenames import Episode, Movie, MultiEpisode
from muxwell.filenames.parser import parse_filename


@pytest.mark.parametrize(
    "filename,expected",
    [
        # Movies
        ## With year
        (
            "The.Matrix.1999.1080p.BluRay.x264-HANDJOB.mkv",
            Movie("The Matrix", 1999),
        ),
        (
            "Inception (2010) 720p BrRip x264 - YIFY.mkv",
            Movie("Inception", 2010),
        ),
        (
            "Parasite.2019.1080p.WEB-DL.H264.AC3-EVO.mkv",
            Movie("Parasite", 2019),
        ),
        (
            "Mad Max Fury Road 2015 2160p HDR BluRay REMUX.mkv",
            Movie("Mad Max Fury Road", 2015),
        ),
        (
            "The.Shawshank.Redemption.1994.MULTi.1080p.BluRay.x264-HDAccess.mkv",
            Movie("The Shawshank Redemption", 1994),
        ),
        (
            "1917.2019.1080p.BluRay.x264.mkv",
            Movie("1917", 2019),
        ),
        (
            "Sonic.the.Hedgehog.2020.2020.1080p.WEB-DL.mkv",
            Movie("Sonic the Hedgehog 2020", 2020),
        ),
        ## Without year
        (
            "Interstellar.1080p.BluRay.x264.mkv",
            None,
        ),
        # TV Episodes
        ## Compact format (S##E##)
        (
            "Breaking.Bad.S01E01.1080p.BluRay.x264-SHORTBREHD.mkv",
            Episode("Breaking Bad", 1, 1),
        ),
        (
            "Game.of.Thrones.S03E10.720p.HDTV.x264-CTU.mkv",
            Episode("Game of Thrones", 3, 10),
        ),
        (
            "The.Mandalorian.S02E04.Chapter.12.DV.2160p.WEB-DL.DDP5.1.HDR.HEVC-TEPES.mkv",
            Episode("The Mandalorian", 2, 4),
        ),
        (
            "Friends - S06E11 - The One With the Apothecary Table.avi",
            Episode("Friends", 6, 11),
        ),
        (
            "Westworld.S03E05.Genre.1080p.AMZN.WEB-DL.DDP5.1.H.264-NTb.mkv",
            Episode("Westworld", 3, 5),
        ),
        (
            "The.Eric.Andre.Show.S06E01.1080p.HEVC.x265-MeGusta[eztv.re].mkv",
            Episode("The Eric Andre Show", 6, 1),
        ),
        (
            "Mr.Robot.S03E08.eps3.7_dont-delete-me.ko.1080p.10bit.WEBRip.6CH.x265.HEVC-PSA.mkv",
            Episode("Mr Robot", 3, 8),
        ),
        (
            "Mr.Robot.S01E09.eps1.8_m1rr0r1ng.qt",
            Episode("Mr Robot", 1, 9),
        ),
        (
            "Mr.Robot.S04E10.410.Gone.1080p.10bit.WEBRip.6CH.x265.HEVC-PSA.mkv",
            Episode("Mr Robot", 4, 10),
        ),
        (
            "Love.Death.and.Robots.S02E08.the.Drowned.Giant.1080p.NF.WEB-DL.DD+5.1.Atmos.HDR.HEVC-L0L.mkv",
            Episode("Love Death and Robots", 2, 8),
        ),
        (
            "The.100.S07E14.1080p.WEB.H264.mkv",
            Episode("The 100", 7, 14),
        ),
        (
            "24.S01E01.1080p.BluRay.x264.mkv",
            Episode("24", 1, 1),
        ),
        ## x format (##x##)
        (
            "Stranger.Things.01x03.1080p.NF.WEB-DL.DDP5.1.H.264-NTb.mkv",
            Episode("Stranger Things", 1, 3),
        ),
        (
            "The.Crown.04x10.The.Waldorf.Astoria.2160p.NF.WEB-DL.DDP5.1.Atmos.DV.HDR.HEVC-TBD.mkv",
            Episode("The Crown", 4, 10),
        ),
        ## Episode format (Episode ##)
        (
            "[bonkai77].Neon.Genesis.Evangelion.Episode.01.[BD.1080p.Dual-Audio.x265.HEVC.10bit].mkv",
            Episode("Neon Genesis Evangelion", 1, 1),
        ),
        (
            "[bonkai77].Kill.la.Kill.Episode.18.Into.the.Night.1080p.Dual.Audio.Bluray.mkv",
            Episode("Kill la Kill", 1, 18),
        ),
        # Multi-Episodes
        ## list format (S##E##E##)
        (
            "The.Simpsons.S25E01E02.720p.HDTV.x264-2HD.mkv",
            MultiEpisode("The Simpsons", 25, [1, 2]),
        ),
        (
            "South.Park.S15E03E04E05.720p.HDTV.x264-aAF.mkv",
            MultiEpisode("South Park", 15, [3, 4, 5]),
        ),
        (
            "Rick.and.Morty.S04E01E02.1080p.WEB-DL.x264.mkv",
            MultiEpisode("Rick and Morty", 4, [1, 2]),
        ),
        (
            "Doctor.Who.2005.S12E05E06.1080p.HDTV.H264.mkv",
            MultiEpisode("Doctor Who 2005", 12, [5, 6]),
        ),
        ## range format (S##E##-E##)
        (
            "The.Office.S03E01-E02.DVDRip.XviD-FLAWL3SS.mkv",
            MultiEpisode("The Office", 3, [1, 2]),
        ),
        # Empty or malformed filenames
        ("", None),
        ("just.a.random.string.mkv", None),
    ],
)
def test_filename_parser(filename: str, expected: object):
    """Test the filename parser with various inputs."""
    result = parse_filename(filename)
    assert (
        result == expected
    ), f"Expected {expected} but got {result} for filename: {filename}"
