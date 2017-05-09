import fnmatch
import os
import os.path


def find_matching(root_path,
                  relative_paths_to_search,
                  file_pattern):
    """
    Given an absolute `root_path`, a list of relative paths to that
    absolute root path (`relative_paths_to_search`), and a `file_pattern`
    like '*.sql', returns information about the files. For example:

    > find_matching('/root/path', 'models', '*.sql')

      [ { 'absolute_path': '/root/path/models/model_one.sql',
          'relative_path': 'models/model_one.sql',
          'searched_path': 'models' },
        { 'absolute_path': '/root/path/models/subdirectory/model_two.sql',
          'relative_path': 'models/subdirectory/model_two.sql',
          'searched_path': 'models' } ]
    """
    matching = []

    for relative_path_to_search in relative_paths_to_search:
        absolute_path_to_search = os.path.join(
            root_path, relative_path_to_search)
        walk_results = os.walk(absolute_path_to_search)

        for current_path, subdirectories, local_files in walk_results:
            for local_file in local_files:
                absolute_path = os.path.join(current_path, local_file)
                relative_path = os.path.relpath(
                    absolute_path, absolute_path_to_search)

                if fnmatch.fnmatch(local_file, file_pattern):
                    matching.append({
                        'searched_path': relative_path_to_search,
                        'absolute_path': absolute_path,
                        'relative_path': relative_path,
                    })

    return matching


def load_file_contents(path, strip=True):
    with open(path, 'rb') as handle:
        to_return = handle.read().decode('utf-8')

    if strip:
        to_return = to_return.strip()

    return to_return
