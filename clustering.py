# needed imports
# needed imports
import sys
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
import Extraction

""" @param: numbers_ofcluster # int, how many group of people you think there are!!! 1-2-3-4
Default is 4:
   no comments - no reactions
   no comments - yes reactions
   yes comments - yes reactions
   yes comments - no reactions
   """
def showCluster(numbers_ofcluster = 6):
    ex = Extraction.Extraction()
    data = Extraction.Extraction()._df
    # Get the dataframe that stores only total number of commments and reactions per user (without user name)
    a = ex.getFriendsCommentReactTotalDFOnly()

    # Initialize the model with 2 parameters -- number of clusters and random state.
    kmeans_model = KMeans(n_clusters=numbers_ofcluster, random_state=100) # random_state is a kind of rerun the process to find the good results
    # Get only the numeric columns from games.
    good_columns = a._get_numeric_data()
    # Fit the model using the good columns.
    kmeans_model.fit(a)
    # Get the cluster assignments.
    labels=kmeans_model.labels_

    # Create a PCA model. This to ensure that data are in 2D instead of 3D
    pca_2 = PCA(2)
    # Fit the PCA model on the numeric columns from earlier.
    plot_columns = pca_2.fit_transform(mat)
    #print(plot_columns[:,0])
    #print(a[:,0])

    # Make a scatter plot of each game, shaded according to cluster assignment.
    plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1],c=labels)
    # Show
    plt.show()


showCluster()

#plt.hist(a['comments'])
#plt.show()
#plt.hist(a['reactions'])
#plt.show()
