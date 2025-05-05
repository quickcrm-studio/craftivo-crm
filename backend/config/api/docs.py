from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.conf import settings

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@renderer_classes([JSONRenderer, TemplateHTMLRenderer])
def api_version_info(request):
    """
    View to provide information about the API versioning.
    """
    version_info = {
        'current_version': settings.REST_FRAMEWORK.get('DEFAULT_VERSION', 'v1'),
        'available_versions': settings.REST_FRAMEWORK.get('ALLOWED_VERSIONS', ['v1']),
        'version_paths': {
            'v1': {
                'url_format': '/api/v1/',
                'endpoints': [
                    '/api/v1/customers/',
                    '/api/v1/products/',
                    '/api/v1/categories/',
                    '/api/v1/orders/',
                    '/api/v1/dashboard/',
                    '/api/v1/auth/login/',
                    '/api/v1/auth/user/',
                    '/api/v1/auth/logout/',
                ]
            }
        },
        'versioning_scheme': 'URL path versioning',
        'description': 'The API uses URL path versioning to maintain backward compatibility as the API evolves.',
        'docs': {
            'description': 'API documentation endpoints',
            'endpoints': [
                '/api/docs/',
                '/api/schema/',
            ]
        }
    }
    
    if request.accepted_renderer.format == 'html':
        return Response(version_info, template_name='api/version_info.html')
    
    return Response(version_info) 