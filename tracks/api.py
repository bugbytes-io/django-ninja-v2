from typing import List, Optional
from ninja import NinjaAPI
from tracks.models import Track
from tracks.schema import TrackSchema, NotFoundSchema

api = NinjaAPI()

@api.get("/test")
def test(request):
    return {'message': 'success!'}


@api.get("/tracks", response=List[TrackSchema])
def tracks(request, title: Optional[str] = None):
    if title:
        return Track.objects.filter(title__icontains=title)
    return Track.objects.all()

@api.get("/tracks/{track_id}", response={200: TrackSchema, 404: NotFoundSchema})
def track(request, track_id: int):
    try:
        track = Track.objects.get(pk=track_id)
        return 200, track
    except Track.DoesNotExist as e:
        return 404, {"message": "Could not find track"}


@api.post("/tracks", response={201: TrackSchema})
def create_track(request, track: TrackSchema):
    # curl -X POST -d '{"artist": "Sonic Youth", "title": "Silver Rocket", "last_play": "2017-10-18 15:15:26", "duration": 200}' http://localhost:8000/api/tracks
    Track.objects.create(**track.dict())
    return track

@api.put("/tracks/{track_id}", response={200: TrackSchema, 404: NotFoundSchema})
def change_track(request, track_id: int, data: TrackSchema):
    # curl -X PUT -d '{"artist": "The Fall", "title": "Silver Rocket", "last_play": "2017-10-18 15:15:26", "duration": 200}' http://localhost:8000/api/tracks/7729
    try:
        track = Track.objects.get(pk=track_id)
        for attribute, value in data.dict().items():
            setattr(track, attribute, value)
        track.save()
        return 200, track
    except Track.DoesNotExist as e:
        return 404, {"message": "Could not find track"}
    

@api.delete("/tracks/{track_id}", response={200: None, 404: NotFoundSchema})
def delete_track(request, track_id: int):
    # curl -X DELETE http://localhost:8000/api/tracks/7729
    try:
        track = Track.objects.get(pk=track_id)
        track.delete()
        return 200
    except Track.DoesNotExist as e:
        return 404, {"message": "Could not find track"}
    