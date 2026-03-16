"""Tests for AutoMatchSubs action."""

from __future__ import annotations

from pathlib import Path

import pytest
import typer

from muxwell.actions.auto_match_subs import AutoMatchSubs
from muxwell.actions.base import ActionContext

MOVIE1_VID = "The.Matrix.1999.1080p.BluRay.mkv"
MOVIE1_VID_ALT = "The.Matrix.1999.mkv"
MOVIE1_EN_SUB = "The.Matrix.1999.eng.srt"
MOVIE1_FR_SUB = "The.Matrix.1999.fr.srt"

MOVIE2_NO_YEAR_VID = "Inception.1080p.BluRay.mkv"
MOVIE2_SUB = "Inception.2010.eng.srt"


EP_S1E1_VID = "Breaking.Bad.S01E01.1080p.BluRay.mkv"
EP_S1E1_SRT = "Breaking.Bad.S01E01.eng.srt"
EP_S1E2_SUB = "Breaking.Bad.S01E02.eng.srt"
EP_S2E1_SUB = "Breaking.Bad.S02E01.eng.srt"

AHS_S2E1_VID = "American.Horror.Story.S02E01.1080p.BluRay.x265-n0m1.mkv"
AHS_S2E1_SUB = "American.horror.story.S02E01.Blu-ray.English-WWW.MY-SUBS.CO.srt"

MULTI_EP_VID = "Friends.S02E01E02.1080p.BluRay.mkv"
MULTI_EP_SUB = "Friends.S02E01E02.eng.srt"


class TestAutoMatchSubs:
    """Test AutoMatchSubs action."""

    def test_file_target_raises(self, file_action_ctx: ActionContext):
        """Test that providing a file target raises an error."""
        action = AutoMatchSubs()
        with pytest.raises(
            typer.BadParameter,
            match="auto-match-subs can only be used with directories.",
        ):
            action.analyze(file_action_ctx)

    @pytest.mark.parametrize(
        ("video_names", "sub_names", "expected"),
        [
            # Matches
            (  ## Movie
                [MOVIE1_VID],
                [MOVIE1_EN_SUB],
                {MOVIE1_VID: [MOVIE1_EN_SUB]},
            ),
            (  ## TV episode
                [EP_S1E1_VID],
                [EP_S1E1_SRT],
                {EP_S1E1_VID: [EP_S1E1_SRT]},
            ),
            (  ## TV episode with different casing
                [AHS_S2E1_VID],
                [AHS_S2E1_SUB],
                {AHS_S2E1_VID: [AHS_S2E1_SUB]},
            ),
            (  ## TV Multi-episode
                [MULTI_EP_VID],
                [MULTI_EP_SUB],
                {MULTI_EP_VID: [MULTI_EP_SUB]},
            ),
            (  ## Multiple subs for one video
                [MOVIE1_VID],
                [MOVIE1_EN_SUB, MOVIE1_FR_SUB],
                {MOVIE1_VID: [MOVIE1_EN_SUB, MOVIE1_FR_SUB]},
            ),
            (  ## Multiple videos and subs with some matches
                [MOVIE1_VID, MOVIE1_VID_ALT],
                [MOVIE1_EN_SUB, MOVIE2_SUB],
                {MOVIE1_VID: [MOVIE1_EN_SUB], MOVIE1_VID_ALT: [MOVIE1_EN_SUB]},
            ),
            # Mismatches
            ## Different movies
            ([MOVIE1_VID], [MOVIE2_SUB], {}),
            ## TV episode with wrong episode number
            ([EP_S1E1_VID], [EP_S1E2_SUB], {}),
            ## TV episode with wrong season number
            ([EP_S1E1_VID], [EP_S2E1_SUB], {}),
            ## Mixed content types
            ([MOVIE1_VID], [EP_S1E1_SRT], {}),
            # Unparseable
            ([MOVIE2_NO_YEAR_VID], [MOVIE2_SUB], {}),
        ],
        ids=[
            "matched_movie",
            "matched_tv_episode",
            "matched_tv_episode_casing",
            "matched_multi_episode",
            "matched_multiple_subs",
            "matched_multiple_videos_subs",
            "mismatched_movies",
            "mismatched_tv_episode",
            "mismatched_tv_season",
            "mixed_content_types",
            "movie_without_year",
        ],
    )
    def test_analyze(
        self,
        empty_dir_action_ctx: ActionContext,
        video_names: list[str],
        sub_names: list[str],
        expected: dict[str, list[str]],
    ):
        """Test matching subtitles for different content types."""
        empty_dir_action_ctx.video_files = [Path(name) for name in video_names]
        empty_dir_action_ctx.subtitles_files = [Path(name) for name in sub_names]
        result = AutoMatchSubs().analyze(empty_dir_action_ctx)
        assert {
            video_path.name: [op.path.name for op in ops]
            for video_path, ops in result.items()
        } == expected
