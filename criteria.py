from nio.common.block.base import Block
from nio.metadata.properties.holder import PropertyHolder
from nio.metadata.properties.list import ListProperty
from nio.metadata.properties.string import StringProperty


class Criterion(PropertyHolder):

    """ Each instance of this class represents a matching criterion
    for Publisher/Subscriber blocks.

    Properties:
        keyword (str): the identifier for the criterion
        rules (list(str)): valid match values

    """
    keyword = StringProperty(title='Keyword', default='')
    rule = ListProperty(StringProperty, title='Rule (list of acceptable values)')


class CriteriaBlock(Block):

    """ Base class for blocks that contain a list of criteria.

    Properties:
        criteria (list(Criterion)): A list of criteria to be used
            as needed.

    """
    criteria = ListProperty(Criterion, title='Criteria')

    def _flatten_criteria(self):
        result = {}
        for c in self.criteria:
            tmp = c.to_dict()
            result[tmp['keyword']] = tmp['rule']
        return result
