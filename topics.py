from nio import Block
from nio.properties import PropertyHolder, ListProperty, StringProperty
from nio.types import StringType


class Criterion(PropertyHolder):

    """ Each instance of this class represents a matching criterion
    for Publisher/Subscriber blocks.

    Properties:
        keyword (str): the identifier for the criterion
        rules (list(str)): valid match values

    """
    keyword = StringProperty(title='Filter Key', default='')
    rule = ListProperty(StringType,
                        title='Filter Values (list of acceptable values)',
                        default=[])


class TopicsBlock(Block):

    """ Base class for blocks that contain a list of criteria.

    Properties:
        criteria (list(Criterion)): A list of criteria to be used
            as needed.

    """
    criteria = ListProperty(Criterion, title='Topics', default=[])

    def _flatten_topics(self):
        result = {}
        for c in self.criteria():
            tmp = c.to_dict()
            result[tmp['keyword']] = tmp['rule']
        return result
