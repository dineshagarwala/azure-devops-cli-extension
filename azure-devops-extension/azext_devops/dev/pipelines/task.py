
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError
from vsts.exceptions import VstsServiceError
from azext_devops.dev.common.services import (get_task_agent_client,
                                      resolve_instance)
from azext_devops.dev.common.uuid import is_uuid


def task_list(team_instance=None, task_id=None, detect=None):
    """List tasks.
    :param team_instance: Azure Devops organization URL. Example: https://dev.azure.com/MyOrganizationName/
    :type team_instance: str
    :param str task_id: The UUID of the task.
    :param detect: Automatically detect values for instance and project. Default is "on".
    :type detect: str
    :rtype: [TaskDefinition]
    """
    try:
        if task_id is not None and not is_uuid(task_id):
            raise ValueError("The --id argument must be a UUID.")
        team_instance = resolve_instance(detect=detect, team_instance=team_instance)
        client = get_task_agent_client(team_instance)
        definition_references = client.get_task_definitions(task_id=task_id)
        return definition_references
    except VstsServiceError as ex:
        raise CLIError(ex)


def task_show(task_id, version, team_instance=None, detect=None):
    """Show task.
    :param str task_id: The UUID of the task.
    :param str version: The version of the task.
    :param team_instance: Azure Devops organization URL. Example: https://dev.azure.com/MyOrganizationName/
    :type team_instance: str
    :param detect: Automatically detect values for instance and project. Default is "on".
    :type detect: str
    :rtype: TaskDefinition
    """
    try:
        if not is_uuid(task_id):
            raise ValueError("The --id argument must be a UUID.")
        team_instance = resolve_instance(detect=detect, team_instance=team_instance)
        client = get_task_agent_client(team_instance)
        definition_references = client.get_task_definition(task_id=task_id,
                                                            version_string=version)
        return definition_references
    except VstsServiceError as ex:
        raise CLIError(ex)
