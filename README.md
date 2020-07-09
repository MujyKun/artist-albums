# Grab Spotify Artist Albums and Songs


This program allows users to access the `/artist/{artist-id}` endpoint and get back a JSON of the Singles and Albums
from that artist as well as the songs in those albums and filtering out specific albums.
  
Hosted on port `5454` (``http://127.0.0.1:5454``)

## Endpoint:
- `/artist/{artist-id}` - The artist id is expected to be spotify's artist id.

## Optional:

This is the expected JSON format for existing albums  
Any albums in this body will be removed from the request.
```
Name of the key value does not matter.
{
    "album1": album-id,
    "album2": album-id,
    ...
}
```