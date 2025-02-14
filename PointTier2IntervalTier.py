"""
Convert PointTier with Points into IntervalTier with Intervals of length zero.
They look broken in Praat but should be processable with Python.
author: Saskia Wepner
date: 2022-November-15
"""
import os
import tgt

inputPath = "path/to/TextGrid/with/PointTier"
# leave outputPath empty if you want to use the same directory for saving; file is renamed then.
outputPath = ""


def main(inPath, outPath):

    # set output path if necessary
    if not outPath:
        outPath = inPath;
        fNameEnding = "_new"
    else:
        fNameEnding = "";
        os.makedirs(outPath, exist_ok=True)

    # search directory for all files that end with ".TextGrid"
    tGrids = [fn for fn in os.listdir(inPath) if fn.endswith(".TextGrid")];
    # go through all textgrids
    for fName in tGrids:
        tGrid = tgt.read_textgrid(f"{inPath}/{fName}", encoding="utf-8");
        # define new file name to avoid overwriting of input file
        fNameNew = fName.split('.')[0] + f"{fNameEnding}.TextGrid";
        # create new, empty textgrid
        tGridNew = tgt.TextGrid(filename=fNameNew);
        # go through all tiers
        for tier in tGrid.tiers:
            # if current tier is a PointTier, we take all Points and convert them to Intervals
            if tier.tier_type() == "PointTier" or tier.tier_type() == "TextTier":
                annotations = []
                # go through all annotations (i.e., Points) on the PointTier
                for annotation in tier.annotations:
                    annotations.append(tgt.Interval(start_time=annotation.start_time, end_time=annotation.end_time,
                                                    text=annotation.text));
                # create new Interval(!)Tier
                tierNew = tgt.IntervalTier(start_time=tier.start_time, end_time=tier.end_time, name=tier.name,
                                           objects=annotations);
            else: # if current tier is an IntervalTier, we just copy it and change nothing
                tierNew = tier;

            # append the tier with all its elements (i.e., intervals)
            tGridNew.add_tier(tierNew);

        # save new textgrid
        tgt.write_to_file(tGridNew, filename=f"{outPath}/{fNameNew}", format="long", encoding="utf-8");


if __name__ == '__main__':
    main(inputPath, outputPath)

