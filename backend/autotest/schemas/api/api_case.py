import typing
from typing import Optional, List
from pydantic import BaseModel, Field, model_validator

from autotest.schemas.api.api_info import ApiBaseSchema, ApiInfoIn
from autotest.schemas.base import BaseSchema
from autotest.schemas.step_data import TStepData


class ApiCaseQuery(BaseSchema):
    """用例查询"""
    id: Optional[int] = Field(None, description="")
    ids: Optional[List[int]] = Field(None, description="")
    name: Optional[str] = Field(None, description="")
    module_name: Optional[str] = Field(None, description="")
    project_name: Optional[str] = Field(None, description="")
    project_id: Optional[int] = Field(None, description="项目id")
    project_ids: Optional[List[int]] = Field(None, description="项目ids")
    order_field: Optional[str] = Field(None, description="")
    created_by: Optional[int] = Field(None, description="")
    created_by_name: Optional[str] = Field(None, description="")
    suite_type: Optional[int] = Field(None, description="")
    user_ids: Optional[List[int]] = Field(None, description="user ids")


class ApiCaseIdsQuery(BaseSchema):
    """用例查询"""
    ids: typing.List[int] = Field(None, description="")


class ApiCaseListSchema(BaseSchema):
    """用例列表"""
    name: str = Field(None, description="")
    project_name: str = Field(None, description="")
    project_id: int = Field(None, description="")
    include: str = Field(None, description="")
    remarks: str = Field(None, description="")
    config_id: int = Field(None, description="")
    run_status: str = Field(None, description="")

    @model_validator(mode='before')
    @classmethod
    def root_validator(cls, data):
        if 'include' in data:
            data['include'] = list(map(int, data['include'].split(','))) if data['include'] else []
        return data


class TCaseRequestData(BaseModel):
    """用例请求数据 前端保存的 api id"""
    api_id: typing.Union[str, int] = Field(None, description="api id")
    name: str = Field(None, description="用例名称")
    method: str = Field(None, description="请求方法")


class TCaseStepData(TStepData):
    """测试用例数据"""
    sub_steps: typing.List['TCaseStepData'] = Field([], description="子步骤， 当前字段只对 if  loop 类型有效")
    # request: TCaseRequestData = Field(None, description="引用用例")


TCaseStepData.update_forward_refs()


class ApiCaseIn(BaseModel):
    """用例保存"""
    id: int = Field(None, description="")
    name: str = Field(None, description="")
    env_id: str = Field(None, description="")
    project_id: int = Field(None, description="")
    remarks: str = Field(None, description="")
    step_rely: int = Field(1, description="")
    step_data: typing.List[ApiInfoIn] = Field(None, description="步骤类容")
    headers: typing.List[ApiBaseSchema] = Field(None, description="请求头参数")
    variables: typing.List[ApiBaseSchema] = Field(None, description="变量参数")
    version: int = Field(None, description="")


class TestCaseRun(BaseModel):
    id: int = Field(None, description="")
    name: str = Field(None, description="")
    env_id: typing.Union[int, str] = Field(None, description="")
    project_id: int = Field(None, description="")
    module_id: int = Field(None, description="")
    remarks: str = Field(None, description="")
    step_data: typing.List[TStepData] = Field([], description="步骤数据")
    step_rely: bool = Field(True, description="步骤依赖 True依赖，False 不依赖")
    headers: typing.List[ApiBaseSchema] = Field(None, description="请求头参数")
    variables: typing.List[ApiBaseSchema] = Field(None, description="变量参数")


class ApiCaseId(BaseSchema):
    id: int = Field(..., description="")


class ApiTestCaseRun(BaseSchema):
    id: int = Field(..., description="用例id")
    env_id: int = Field(None, description="环境id")


class ApiCaseStepDataSchema(TStepData):
    api_id: int = Field(None, description="api_id")
    step_data: TStepData = Field(None, description="步骤数据")
