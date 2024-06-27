from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .utils import fetch_arxiv_data, parse_arxiv_response, create_snapshot
import os

class ArxivSearchView(APIView):
    def get(self, request):
        query = request.GET.get('query', '')
        try:
            xml_response = fetch_arxiv_data(query)
            print("Fetched XML response:", xml_response)
        except Exception as e:
            print("Error fetching data:", e)
            return Response({"message": "Error fetching data"})
        
        try:
            parsed_data = parse_arxiv_response(xml_response)
            print("Parsed Data:", parsed_data)
        except Exception as e:
            print("Error parsing data:", e)
            return Response({"message": "Error parsing data"})
        
        if parsed_data:
            try:
                images = []
                for index, entry in enumerate(parsed_data):  # Limit to 6 results
                    print("Entry:", entry)
                    img_path = create_snapshot(entry['title'], entry['summary'], entry['pdf_link'], index)
                    relative_img_path = os.path.relpath(img_path, settings.SNAPSHOTS_ROOT)
                    images.append([f"{settings.SNAPSHOTS_URL}{relative_img_path}", entry['pdf_link']])
                return Response({"img_paths": images}, status=200)
            except Exception as e:
                print("Error creating snapshot:", e)
                return Response({"message": "Error creating snapshot"})
        
        return Response({"message": "No data found"})
