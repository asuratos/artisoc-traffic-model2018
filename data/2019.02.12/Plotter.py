import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import os
import glob

sns.set()
outputext = "eps"

try:
    os.mkdir("plots")
except:
    pass

#Phantom Jams
# Check if user wants to plot Jams
plot = input("Plot Phantom Jams (y/n)?")

if plot == "Y" or plot == "y":
    #Prepare relevant plot directories
    try:
        os.mkdir("plots\Jams")
    except:
        pass

    try:
        os.mkdir("plots\Jams\\"+outputext)
    except:
        pass
    

    jamdata = pd.read_csv("Jams.csv")

    for reaction in jamdata["Reaction"].unique():
        for density in jamdata["Total Cars"].unique():
            for asocialrate in jamdata["ASocial Rate"].unique():

                dataslice = jamdata[(jamdata["Total Cars"] == density) & 
                            (jamdata["Reaction"] == reaction) & 
                            (jamdata["ASocial Rate"] == asocialrate)]


                sns.scatterplot(x = "Time", 
                            y = "Y", 
                            s = 20,
                            data = dataslice[~dataslice["ASocial"]],
                            label = "Social")
                sns.scatterplot(x = "Time", 
                            y = "Y", 
                            s = 20,
                            data = dataslice[dataslice["ASocial"]],
                            label = "ASocial")  
                
                social_count = dataslice[~dataslice["ASocial"]]["ASocial"].count()

                asocial_count = dataslice[dataslice["ASocial"]]["ASocial"].count()


                total = social_count + asocial_count
                
                # asocial_count = jamdata[(jamdata["Total Cars"] == density) & 
                #                         (jamdata["Reaction"] == reaction) & 
                #                         (jamdata["ASocial Rate"] == asocialrate)]["ASocial"].count()
                
                # social_count = jamdata[(jamdata["Total Cars"] == density) & 
                #                         (jamdata["Reaction"] == reaction) & 
                #                         (jamdata["ASocial Rate"] == asocialrate)]["ASocial"].count()

                plt.title("Location of Traffic Jams\n(%s cars, %s asocial rate, %s reaction time)\n%s Social, %s ASocial (%.2f)" % 
                            (density, asocialrate, reaction, social_count, asocial_count, float(asocial_count/(total)) if total != 0 else 0))
        
                plt.xlabel("Time (s)")
                plt.ylabel("Position on Road")
        
                plt.xlim(xmin = jamdata["Time"].min(), xmax = jamdata["Time"].max())
                plt.ylim(ymin = 0, ymax = 300)
        
                plt.savefig("plots\Jams\\" 
                            + outputext 
                            + "\jamlocation_%scars_%sasocial_%sreaction." % (density, asocialrate, reaction) 
                            + outputext,
                            bbox_inches="tight")
                plt.clf()
                #plt.show()

    print("Jam Plotting Done!")

#Speed Time Series

# Check if user wants to plot Speed Time Series
plot = input("Plot Speed Time Series (y/n)?")

if plot == "Y" or plot == "y":
    #Prepare relevant plot directories
    try:
        os.mkdir("plots\SpeedSeries")
    except:
        pass

    try:
        os.mkdir("plots\SpeedSeries\\"+outputext)
    except:
        pass

    speeds = pd.read_csv("singlecar.csv")

    for reaction in speeds["Reaction"].unique():
        for density in speeds["TotalCars"].unique():
            for asocialrate in speeds["ASocial Rate"].unique(): 
                
                dataslice = speeds[(speeds["Reaction"] == reaction) &
                                (speeds["ASocial Rate"] == asocialrate) &
                                (speeds["TotalCars"] == density)]
                
                for asocial in dataslice["ASocial"].unique():
                    sns.lineplot(x = "Lifetime", 
                                y = "Speed",
                                data = dataslice[dataslice["ASocial"] == asocial],
                                err_style = None)

                    plt.title("Speed for a single car\n(%s cars, %s asocial rate, %s reaction, %s)" 
                            % (density, asocialrate, reaction, "ASocial" if asocial else "Social"))

                    plt.ylim(ymin = 0)
                    plt.xlim(xmin = 0, xmax = dataslice[dataslice["ASocial"] == asocial]["Lifetime"].max())
                    
                    plt.xlabel("Time (s)")
                    plt.ylabel("Speed (km/h)")

                    plt.savefig("plots\SpeedSeries\\"
                                + outputext
                                + "\speedseries_%scars_%sasocialrate_%sreaction_%s." 
                                % (density, asocialrate, reaction, "asocial" if asocial else "social")
                                + outputext,
                                bbox_inches="tight")

                    
                    plt.clf()
                    #plt.show()
                
    print("Speed Time Series Done!")

# Congestion
# Check if user wants to plot congestion
plot = input("Plot congestion (y/n)?")

if plot == "Y" or plot == "y":

    #Prepare relevant plot directories
    try:
        os.mkdir("plots\congestion")
    except:
        pass

    try:
        os.mkdir("plots\congestion\\"+outputext)
    except:
        pass

    speeddata = pd.read_csv("speeds.csv")

    for asocialrate in speeddata["ASocial Rate"].unique():
        dataslice = speeddata[speeddata["ASocial Rate"] == asocialrate]
        sns.lineplot(x = "Total Cars", 
                    y = "Slowed", 
                    data = dataslice,
                    style = "ASocial",
                    hue = dataslice["Reaction Time"].replace(dataslice["Reaction Time"].unique(), ["Instant", "Normal", "Slow"]),
                    err_style= None)

        plt.title("Ratio of slowed cars (%s asocial rate)" % asocialrate)
        

        plt.xlim(xmin = dataslice["Total Cars"].min(), xmax = dataslice["Total Cars"].max())
        plt.ylim(ymin = 0, ymax = 1)
        
        plt.ylabel("Ratio of Cars Slowed")
        
        plt.savefig("plots\congestion\\"
                +outputext
                +"\congestion_%sasocialrate." % asocialrate
                +outputext,
                bbox_inches="tight")
        plt.clf()
        #plt.show()

    print("Congestion Plots Done!")