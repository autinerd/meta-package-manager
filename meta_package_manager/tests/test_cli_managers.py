# -*- coding: utf-8 -*-
#
# Copyright Kevin Deldycke <kevin@deldycke.com> and contributors.
# All Rights Reserved.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

# pylint: disable=redefined-outer-name

import pytest
import simplejson as json

from .conftest import MANAGER_IDS
from .test_cli import \
    test_manager_selection  # Run manager selection tests for this subcommand.
from .test_cli import check_manager_selection


@pytest.fixture
def subcommand():
    return 'managers'


def test_default_all_manager(invoke, subcommand):
    result = invoke(subcommand)
    assert result.exit_code == 0
    check_manager_selection(result.output)


@pytest.mark.parametrize('mid', MANAGER_IDS)
def test_single_manager(invoke, subcommand, mid):
    result = invoke('--manager', mid, subcommand)
    assert result.exit_code == 0
    check_manager_selection(result.output, {mid})


def test_json_parsing(invoke, subcommand):
    result = invoke('--output-format', 'json', subcommand)
    assert result.exit_code == 0
    data = json.loads(result.output)

    assert data
    assert isinstance(data, dict)
    assert set(data) == MANAGER_IDS

    for manager_id, info in data.items():
        assert isinstance(manager_id, str)
        assert isinstance(info, dict)

        assert set(info) == {
            'available', 'cli_path', 'errors', 'executable', 'fresh', 'id',
            'name', 'supported', 'version'}

        assert isinstance(info['available'], bool)
        if info['cli_path'] is not None:
            assert isinstance(info['cli_path'], str)

        assert isinstance(info['errors'], list)
        if info['errors']:
            assert set(map(type, info['errors'])) == {str}

        assert isinstance(info['executable'], bool)
        assert isinstance(info['fresh'], bool)
        assert isinstance(info['id'], str)
        assert isinstance(info['name'], str)
        assert isinstance(info['supported'], bool)

        if info['version'] is not None:
            assert isinstance(info['version'], str)

        assert info['id'] == manager_id
