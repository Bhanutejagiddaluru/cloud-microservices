# optional standalone training script
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import joblib

def main():
    data = load_iris()
    X, y = data.data, data.target
    clf = LogisticRegression(max_iter=200)
    clf.fit(X, y)
    joblib.dump(clf, "model.pkl")
    print("Saved model.pkl")

if __name__ == "__main__":
    main()
