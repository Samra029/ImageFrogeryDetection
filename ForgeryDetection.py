from sklearn.cluster import DBSCAN
import numpy as np
import cv2


class Detect(object):
    def __init__(self, input):
        self.image = cv2.imread(input)

    def siftDetector(self):
        sift = cv2.SIFT_create()
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.key_points, self.descriptors = sift.detectAndCompute(gray, None)
        return self.key_points, self.descriptors

    def showSiftFeatures(self):
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        sift_image = cv2.drawKeypoints(
            self.image, self.key_points, self.image.copy())
        return sift_image

    def locateForgery(self, eps=40, min_samples=2):
        clusters = DBSCAN(eps=eps, min_samples=min_samples).fit(self.descriptors)
        # Get the unique cluster labels (ignore -1, which represents noise)
        unique_labels = np.unique(clusters.labels_)
        unique_labels = unique_labels[unique_labels != -1]  # Remove noise label (-1)

        size = len(unique_labels)  # Number of valid clusters
        forgery = self.image.copy()

        if size == 0:
            print('No Forgery Found!!')
            return None

        # Create cluster list with size based on number of clusters
        cluster_list = [[] for _ in range(size)]

        # Group keypoints into their corresponding clusters
        for idx in range(len(self.key_points)):
            if clusters.labels_[idx] != -1:  # Ignore noise points (-1)
                cluster_index = np.where(unique_labels == clusters.labels_[idx])[0][0]
                cluster_list[cluster_index].append(
                    (int(self.key_points[idx].pt[0]), int(self.key_points[idx].pt[1])))

        # Draw lines between points within each cluster
        for points in cluster_list:
            if len(points) > 1:
                for idx1 in range(1, len(points)):
                    # Green color in BGR for highlighting the forgeries
                    cv2.line(forgery, points[0], points[idx1], (0, 255, 0), 5)

        return forgery
