from DataModel import Text, GroupType
from dateutil.relativedelta import relativedelta
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import timedelta


class AsyncClient(AsyncIOMotorClient):
    def __init__(self, db: str = 'admin', host: str = 'localhost', port: str = '27017'):
        super().__init__(f'mongodb://{host}:{port}')
        self.__db = self.get_database(db)

    @property
    def collection(self):
        return self.__db.get_collection('test')

    async def get_data(self, data: Text) -> dict:
        res = {'dataset': [], 'labels': []}
        match data.group_type:
            case GroupType.hour:
                incval = timedelta(hours=1)
            case GroupType.day:
                incval = timedelta(days=1)
            case GroupType.week:
                incval = timedelta(days=7)
            case GroupType.month:
                incval = relativedelta(months=+1)
        lastdate = data.dt_from
        curdate = lastdate + incval
        while curdate <= data.dt_upto:
            pipline = [{'$match': {'dt': {'$gte': lastdate, '$lte': curdate}}},
                       {'$group': {'_id': '1', 'sum': {'$sum': '$value'}}}]
            if agr_list := await self.collection.aggregate(pipline).to_list(1):
                res['dataset'].append(agr_list[0]['sum'])
            else:
                res['dataset'].append(0)

            res['labels'].append(lastdate.isoformat())
            lastdate = curdate
            curdate += incval
        else:
            pipline = [{'$match': {'dt': {'$gte': lastdate, '$lte': data.dt_upto}}},
                       {'$group': {'_id': '1', 'sum': {'$sum': '$value'}, 'count': {'$sum': 1}}}]

            if agr_list := await self.collection.aggregate(pipline).to_list(1):
                res['dataset'].append(agr_list[0]['sum'])
            else:
                res['dataset'].append(0)
            res['labels'].append(lastdate.isoformat())
            return res
