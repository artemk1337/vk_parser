import types
import time
from typing import Union, Optional

from pydantic import BaseModel as BaseFormat, validator

from settings import VK_SESSION, TOOLS, ITER_MAX_BUFFER, PHOTO_MAX_SHIFT_TIME
from utils.export import list2txt


class UserInfoFormat(BaseFormat):
    id: int
    can_access_closed: bool
    sex: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bdate: Optional[str] = None
    last_seen: Optional[Union[int, dict]] = None
    images: Optional[list] = None

    @validator("last_seen")
    def last_seen_reformat(cls, value):
        if value:
            return value.get('time', None)
        return value


class UserPhotosParser:

    def __init__(self, user_id, max_shift_time=PHOTO_MAX_SHIFT_TIME):
        self.user_id = user_id
        self.max_shift_time = max_shift_time

    def parse_all(self) -> list:
        """

        :return:
        >>> UserPhotosParser(139132090).parse_all()
        ['https://sun9-53.userapi.com/impf/c855236/v855236325/b300f/mordyGFgNyo.jpg?size=912x690&quality=96&sign=d01d21b55925551880dd2f579b86d41d&c_uniq_tag=7qp_b56qi2cGNPW6gwAL2vAEd75-_pPaRSrY6AHtqxo&type=album', \
'https://sun9-38.userapi.com/impf/c852024/v852024318/18f769/F0MCg_CbIgg.jpg?size=1280x960&quality=96&sign=498932735a6566f2694e0342e8adc0a9&c_uniq_tag=VyAPsYVA9nWeZyQRI6EbITMooCnONgSNmLcU6OZZW54&type=album', \
'https://sun9-52.userapi.com/impf/c855424/v855424089/7b491/mEZ6F1SonHY.jpg?size=810x1080&quality=96&sign=4d0de2548212efe50d5dbcedb2591518&c_uniq_tag=J91__ep4xL5G38f02lyvJXvZv_lZUCFtxraRZJdxxXI&type=album']

        """
        images = VK_SESSION.get_api().photos.getAll(
            owner_id=self.user_id,
            extended=0
        )['items']
        images = [image['sizes'][-1]['url'] for image in images if time.time() - image['date'] < self.max_shift_time]

        return images


class UserMainInfoParser:

    def __init__(
            self,
            user_ids,
            fields: Union[list, tuple, set] = ('about',
                                               'bdate',
                                               'has_photo',
                                               'sex',
                                               'last_seen',
                                               'online',
                                               'deactivated',
                                               'can_access_closed',
                                               'photo_400_orig',),
    ):
        self.user_ids = user_ids
        self.fields = fields

    def parse_all(self):
        """

        :return:
        >>> UserMainInfoParser((139132090, 148693908)).parse_all()

        """
        users = VK_SESSION.get_api().users.get(
            user_ids=self.user_ids,
            fields=self.fields,
            name_case='nom'
        )
        for i, user in enumerate(users):
            user['images'] = [user['photo_400_orig']]
            users[i] = UserInfoFormat(**user).dict()

        return users


class UserFriendsIdsParser:

    def __init__(self, user_id: int):
        """

        :param user_id:
        """
        self.user_id = user_id

    def parse_all(self) -> list:
        """
        Parse all friend ids.

        :return: dict
        >>> UserFriendsIdsParser(139132090).parse_all()
        {'count': 169, 'items': []}
        """
        return TOOLS.get_all(method="friends.get", max_count=ITER_MAX_BUFFER, values={'user_id': self.user_id})['items']

    def parse_generator(self) -> types.GeneratorType:
        """
        Parse all friend ids.

        :return: generator with id
        """
        return TOOLS.get_all_iter(method="friends.get", max_count=ITER_MAX_BUFFER, values={'user_id': self.user_id})

    def export_txt(self) -> None:
        """
        Export friends to txt file.
        """
        friends_list = self.parse_all()
        list2txt(friends_list, f'data/{self.user_id}_friends.txt')
