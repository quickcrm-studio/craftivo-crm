# API Versioning

This project implements a versioned API structure to ensure backward compatibility as the API evolves over time.

## Versioning Strategy

- **Method**: URL Path Versioning
- **Format**: `/api/v{version_number}/endpoint`
- **Example**: `/api/v1/customers/`

## Available Versions

- **v1**: Initial API version

## How It Works

1. The `VersionedRouter` class in `urls.py` handles organizing routes by version
2. All API endpoints are grouped under their respective version namespace (`/api/v1/`)
3. Django REST Framework's `URLPathVersioning` handles version detection

## Adding a New API Version

To add a new API version (e.g., `v2`):

1. Update the settings in `settings.py`:
   ```python
   'ALLOWED_VERSIONS': ['v1', 'v2'],
   ```

2. Add a new router in `VersionedRouter` class in `urls.py`:
   ```python
   def __init__(self):
       self.v1_router = routers.DefaultRouter()
       self.v2_router = routers.DefaultRouter()
       
       # Register v1 routes
       self.v1_router.register(r'customers', CustomerViewSetV1)
       # ...
       
       # Register v2 routes
       self.v2_router.register(r'customers', CustomerViewSetV2)
       # ...
   ```

3. Add the new version to the `get_urls` method:
   ```python
   def get_urls(self):
       return [
           # ...
           path('v2/', include([
               path('', include(self.v2_router.urls)),
               # v2 specific endpoints
           ])),
           # ...
       ]
   ```

4. Update viewsets to handle the new version:
   ```python
   def get_serializer_class(self):
       api_version = self.request.version
       
       if api_version == 'v1':
           return CustomerSerializerV1
       elif api_version == 'v2':
           return CustomerSerializerV2
       
       # Default fallback
       return CustomerSerializerV1
   ```

## Documentation

API documentation is available at `/api/docs/`

## Implementation Details

- The versioning is implemented using Django REST Framework's built-in versioning system
- Each endpoint checks the requested version and responds accordingly
- New API features should be added to the latest version
- Critical bug fixes should be applied to all supported versions 