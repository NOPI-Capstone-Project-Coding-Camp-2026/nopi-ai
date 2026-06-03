from rapidfuzz.distance import Levenshtein


def calculate_cer(pred_text, gt_text):

    pred_text = pred_text.strip()
    gt_text = gt_text.strip()

    if len(gt_text) == 0:
        return 1.0

    distance = Levenshtein.distance(
        pred_text,
        gt_text
    )

    cer = distance / len(gt_text)

    return round(cer, 4)


def calculate_wer(pred_text, gt_text):

    pred_words = pred_text.split()
    gt_words = gt_text.split()

    if len(gt_words) == 0:
        return 1.0

    distance = Levenshtein.distance(
        pred_words,
        gt_words
    )

    wer = distance / len(gt_words)

    return round(wer, 4)