from django.shortcuts import render
from .forms import ReviewForm
import joblib

# Загрузка моделей
classification_model = joblib.load('reviews/trained_model.pkl')
rating_model_neg = joblib.load('reviews/pipeline_ridge_neg.pkl')
rating_model_pos = joblib.load('reviews/pipeline_ridge_pos.pkl')


def classify_and_predict(review_text):
    # Классификация отзыва
    classification_result = classification_model.predict([review_text])[0]

    # Предсказание рейтинга
    if classification_result == 1:
        rating = rating_model_pos.predict([review_text])[0]
        sentiment = 'positive'
    else:
        rating = rating_model_neg.predict([review_text])[0]
        sentiment = 'negative'

    rating = round(rating, 1)

    return sentiment, rating


def review_view(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_text = form.cleaned_data['review_text']
            # Классификация и предсказание рейтинга
            sentiment, rating = classify_and_predict(review_text)
            # Сохранение отзыва в базе данных
            review = form.save(commit=False)
            review.rating = rating
            review.sentiment = sentiment
            review.save()
            return render(request, 'reviews/result.html', {'rating': rating, 'sentiment': sentiment})
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form})
