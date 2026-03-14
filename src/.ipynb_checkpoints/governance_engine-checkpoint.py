import numpy as np
from sklearn.metrics import accuracy_score


class GovernanceEngine:

    def __init__(self, y_true, y_pred, sensitive_feature):
        self.y_true = np.array(y_true)
        self.y_pred = np.array(y_pred)
        self.sensitive_feature = np.array(sensitive_feature)

    def calculate_accuracy(self):
        accuracy = accuracy_score(self.y_true, self.y_pred) * 100
        return accuracy

    def calculate_imbalance_score(self):
        values, counts = np.unique(self.y_true, return_counts=True)
        imbalance_ratio = min(counts) / sum(counts)

        if imbalance_ratio >= 0.40:
            imbalance_score = 100
        elif imbalance_ratio >= 0.30:
            imbalance_score = 80
        elif imbalance_ratio >= 0.20:
            imbalance_score = 60
        else:
            imbalance_score = 40

        return imbalance_score

    def calculate_fairness(self):

        male_mask = self.sensitive_feature == "M"
        female_mask = self.sensitive_feature == "F"

        male_positive_rate = np.mean(self.y_pred[male_mask])
        female_positive_rate = np.mean(self.y_pred[female_mask])

        fairness_gap = abs(male_positive_rate - female_positive_rate)

        if fairness_gap < 0.05:
            fairness_score = 100
        elif fairness_gap < 0.10:
            fairness_score = 75
        elif fairness_gap < 0.20:
            fairness_score = 50
        else:
            fairness_score = 25

        return fairness_gap, fairness_score

    def calculate_governance_index(self, accuracy, fairness_score, imbalance_score):

        governance_index = (
            0.4 * accuracy +
            0.4 * fairness_score +
            0.2 * imbalance_score
        )

        return governance_index

    def risk_level(self, governance_index):

        if governance_index >= 85:
            return "Low Risk – Production Ready"
        elif governance_index >= 70:
            return "Moderate Risk – Monitor Closely"
        elif governance_index >= 50:
            return "High Risk – Mitigation Required"
        else:
            return "Critical Risk – Do Not Deploy"

    def evaluate(self):

        accuracy = self.calculate_accuracy()

        fairness_gap, fairness_score = self.calculate_fairness()

        imbalance_score = self.calculate_imbalance_score()

        governance_index = self.calculate_governance_index(
            accuracy,
            fairness_score,
            imbalance_score
        )

        risk = self.risk_level(governance_index)

        unique_predictions = len(set(self.y_pred))
        collapse_warning = unique_predictions == 1

        if collapse_warning:
            risk = "Critical Risk – Model Collapse Detected"

        return {
            "accuracy": accuracy,
            "fairness_gap": fairness_gap,
            "fairness_score": fairness_score,
            "imbalance_score": imbalance_score,
            "governance_index": governance_index,
            "risk_level": risk,
            "prediction_collapse": collapse_warning
        }