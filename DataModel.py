from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from datetime import UTC


class GroupType(Enum):
    hour = 'hour'
    day = 'day'
    week = 'week'
    month = 'month'


class Text(BaseModel):
    dt_from: datetime
    dt_upto: datetime
    group_type: GroupType

    @property
    def utcdt_from(self):
        '''
            в базе явно время с таймзоной?
        :return:
        '''
        timestamp = self.dt_from.timestamp()
        return datetime.fromtimestamp(timestamp, UTC)

    @property
    def utcdt_upto(self):
        timestamp = self.dt_upto.timestamp()
        return datetime.fromtimestamp(timestamp, UTC)
