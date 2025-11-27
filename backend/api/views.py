from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .excel_loader import (
    filter_by_area,
    filter_multiple_areas,
    get_trend_for_area
)

from .chatbot import mock_summary


@api_view(['POST'])
def analyze(request):
    """
    Accepts query like:
    - "Analyze Wakad"
    - "Compare Aundh and Baner"
    - "Show price growth for Akurdi"
    """
    query = request.data.get("query", "").strip()

    if not query:
        return Response({"error": "Query is required"}, status=status.HTTP_400_BAD_REQUEST)

    q_lower = query.lower()

    # --------------------
    # Case 1: Analyze <Area>
    # --------------------
    if q_lower.startswith("analyze "):
        area = query[8:].strip()
        df = filter_by_area(area)
        summary = mock_summary(area, df)
        trend = get_trend_for_area(area)
        table = df.to_dict(orient="records")

        return Response({
            "summary": summary,
            "trend": trend,
            "table": table
        })

    # --------------------
    # Case 2: Compare A and B
    # --------------------
    if "compare" in q_lower:
        # Extract area names after "compare"
        text = query.lower().replace("compare", "")
        parts = [part.strip() for part in text.replace("and", ",").split(",") if part.strip()]

        if len(parts) < 2:
            return Response({"error": "Provide at least 2 areas to compare."},
                            status=status.HTTP_400_BAD_REQUEST)

        area1, area2 = parts[:2]

        df = filter_multiple_areas([area1, area2])
        table = df.to_dict(orient="records")

        trend = {
            area1: get_trend_for_area(area1),
            area2: get_trend_for_area(area2)
        }

        summary = f"Comparison between {area1} and {area2}"

        return Response({
            "summary": summary,
            "trend": trend,
            "table": table
        })

    # --------------------
    # Fallback: treat entire query as area name
    # --------------------
    df = filter_by_area(query)
    if not df.empty:
        summary = mock_summary(query, df)
        trend = get_trend_for_area(query)
        table = df.to_dict(orient="records")

        return Response({
            "summary": summary,
            "trend": trend,
            "table": table
        })

    return Response({"error": "Could not understand query."},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def upload_dataset(request):
    """
    Optional endpoint to upload a new dataset.xlsx file.
    """
    file = request.FILES.get("file")

    if not file:
        return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    from django.conf import settings
    import os

    save_path = os.path.join(settings.DATA_DIR, "dataset.xlsx")

    with open(save_path, "wb") as f:
        for chunk in file.chunks():
            f.write(chunk)

    # Clear cached DF
    from . import excel_loader
    excel_loader._df_cache = None

    return Response({"status": "Dataset uploaded successfully"})
