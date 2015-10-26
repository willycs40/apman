from pkg_resources import resource_string
foo_config = resource_string(__name__, 'README.md')

print(foo_config)