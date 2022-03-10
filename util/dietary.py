from collections import Counter


def update_dietary(old: dict, new: dict) -> dict:
  result = old

  for key in result.keys():
    # First, let's make sure what we have is an array of stuff
    if type(result[key]['vegetarian']) == str:
      result[key]['vegetarian'] = [result[key]['vegetarian']]
    if type(result[key]['vegan']) == str:
      result[key]['vegan'] = [result[key]['vegan']]

    # Then, add the new
    if key in new.keys():
      if 'vegetarian' in new[key].keys():
        result[key]['vegetarian'].append(new[key]['vegetarian'])
      if 'vegan' in new[key].keys():
        result[key]['vegan'].append(new[key]['vegan'])

  return result

def select_dietary(items: dict) -> dict:
  def decide(choices: list) -> str:
    counts = Counter(choices)

    # If there is only one choice, return that
    if len(counts.keys()) == 1:
      return choices[0]
    # If we have a 'never', let's say that as a precaution
    elif 'never' in counts.keys():
      return 'never'
    # If at least one source says 'sometimes' while others say 'always', return 'sometimes'
    elif 'sometimes' in counts.keys() and 'always' in counts.keys():
      return 'sometimes'
    # If we have several values, return the most common
    elif len(counts.keys()) > 1:
      return counts.most_common(1)[0]
    # In any other case, just return 'unknown'
    else:
      return 'unknown'

  # Do it for all the items
  result = items

  for key in result.keys():
    result[key]['vegetarian'] = decide(result[key]['vegetarian'])
    result[key]['vegan'] = decide(result[key]['vegan'])

  return result
