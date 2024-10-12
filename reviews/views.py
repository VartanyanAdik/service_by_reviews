from django.shortcuts import render
from .forms import ReviewForm
import joblib


# Загрузка обученной модели
model = joblib.load('reviews/trained_model.pkl')

def review_view(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_text = form.cleaned_data['review_text']
            # Предсказание рейтинга и статуса
            prediction = model.predict([review_text])
            rating = prediction[0]
            sentiment = 'positive' if rating == 1 else 'negative'
            # Сохранение отзыва в базе данных
            review = form.save(commit=False)
            review.rating = rating
            review.sentiment = sentiment
            review.save()
            return render(request, 'reviews/result.html', {'rating': rating, 'sentiment': sentiment})
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form})
