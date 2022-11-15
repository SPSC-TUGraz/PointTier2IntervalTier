# This is a sample Python script.

# Press <no shortcut> to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import tgt

inputPath = "C:/Users/kia/Nextcloud2/BesprechungsordnerAnnelieseSaskia/AgreementStudie/PointTier"
# leave outputPath empty if you want to use the same directory for saving.
outputPath = ""


def print_hi(inPath, outPath):

    # set output path if necessary
    if not outPath:
        outPath = inPath;

    # search directory for all files that end with ".TextGrid"
    tGrids = [fn for fn in os.listdir(inPath) if fn.endswith(".TextGrid")];
    for fName in tGrids:
        tGrid = tgt.read_textgrid(f"{inPath}/{fName}", encoding="utf-8");
        # define new file name to avoid overwriting
        fNameNew = fName.split('.')[0] + "_new.TextGrid";
        # create new, empty textgrid
        tGridNew = tgt.TextGrid(filename=fNameNew);
        for tier in tGrid.tiers:
            if tier.tier_type() == "PointTier" or tier.tier_type() == "TextTier":
                annotations = []
                for annotation in tier.annotations:
                    annotations.append(tgt.Interval(start_time=annotation.start_time, end_time=annotation.end_time,
                                                    text=annotation.text));
                tierNew = tgt.IntervalTier(start_time=tier.start_time, end_time=tier.end_time, name=tier.name,
                                           objects=annotations);
            else: # if current tier is an IntervalTier, we just copy it
                tierNew = tier;

            # append the tier with all its elements (i.e., intervals)
            tGridNew.add_tier(tierNew);

        tgt.write_to_file(tGridNew, filename=f"{outPath}/{fNameNew}", format="long", encoding="utf-8");

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi(inputPath, outputPath)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
