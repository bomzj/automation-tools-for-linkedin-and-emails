DEPTH_LIMIT = 1  # Limit the depth of the crawl
DOWNLOAD_TIMEOUT = 10  # Short timeout to fail fast
RETRY_TIMES = 1  # Only retry once
REDIRECT_MAX_TIMES = 3  # Limit redirect

# Custom settings

# Maximum number of pages to crawl per domain
MAX_PAGES_PER_DOMAIN = 50

# Keywords that indicate a high priority URL to crawl first
PRIORITY_URL_KEYWORDS = [
  'career',
  'job',
  'work',
  'employment',
  'join',
  'opportunity',
  'recruiting',
  'apply',
  'opening',
  'position',
  'talent',
  'vacancy',
  'vacancies',
  'hiring',
  'work',
  'contact',
  'about',
  'connect',
  'team',
  'hiring',
  'hire'
]