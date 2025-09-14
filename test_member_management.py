#!/usr/bin/env python3
"""
Test script for board member management functionality.
This script creates test users and boards, then tests the member management features.
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:5000"
API_BASE = f"{BASE_URL}/api"

def create_test_user(username, email, password, name):
    """Create a test user"""
    data = {
        "username": username,
        "email": email,
        "password": password,
        "name": name
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup", json=data)
    if response.status_code == 201:
        print(f"✅ Created user: {username}")
        return True
    else:
        print(f"❌ Failed to create user {username}: {response.text}")
        return False

def login_user(username, password):
    """Login user and return session cookies"""
    data = {
        "username": username,
        "password": password
    }
    
    session = requests.Session()
    response = session.post(f"{BASE_URL}/auth/login", json=data)
    
    if response.status_code == 200:
        print(f"✅ Logged in user: {username}")
        return session
    else:
        print(f"❌ Failed to login {username}: {response.text}")
        return None

def create_board(session, title):
    """Create a board"""
    data = {
        "title": title,
        "description": "Test board for member management",
        "visibility": "private"
    }
    
    response = session.post(f"{API_BASE}/boards", json=data)
    if response.status_code == 201:
        board_data = response.json()
        print(f"✅ Created board: {title} (ID: {board_data['id']})")
        return board_data
    else:
        print(f"❌ Failed to create board: {response.text}")
        return None

def get_board_members(session, board_id):
    """Get board members"""
    response = session.get(f"{API_BASE}/boards/{board_id}/members")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved board members: {len(data['members'])} members")
        return data
    else:
        print(f"❌ Failed to get board members: {response.text}")
        return None

def invite_member(session, board_id, username_or_email):
    """Invite a member to the board"""
    data = {
        "username_or_email": username_or_email
    }
    
    response = session.post(f"{API_BASE}/boards/{board_id}/members", json=data)
    if response.status_code == 201:
        result = response.json()
        print(f"✅ Invited member: {username_or_email}")
        return True
    else:
        print(f"❌ Failed to invite member {username_or_email}: {response.text}")
        return False

def remove_member(session, board_id, user_id):
    """Remove a member from the board"""
    response = session.delete(f"{API_BASE}/boards/{board_id}/members/{user_id}")
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Removed member (ID: {user_id})")
        return True
    else:
        print(f"❌ Failed to remove member {user_id}: {response.text}")
        return False

def test_non_owner_invite(session, board_id, username_or_email):
    """Test that non-owners cannot invite members"""
    data = {
        "username_or_email": username_or_email
    }
    
    response = session.post(f"{API_BASE}/boards/{board_id}/members", json=data)
    if response.status_code == 403:
        print(f"✅ Non-owner correctly blocked from inviting members")
        return True
    else:
        print(f"❌ Non-owner should not be able to invite members: {response.status_code}")
        return False

def main():
    print("🧪 Testing Board Member Management Functionality")
    print("=" * 50)
    
    # Test users
    users = [
        {"username": "owner_user", "email": "owner@test.com", "password": "password123", "name": "Board Owner"},
        {"username": "member1", "email": "member1@test.com", "password": "password123", "name": "Member One"},
        {"username": "member2", "email": "member2@test.com", "password": "password123", "name": "Member Two"},
    ]
    
    # Create test users
    print("\n📝 Creating test users...")
    for user in users:
        create_test_user(**user)
    
    # Login as board owner
    print("\n🔐 Logging in as board owner...")
    owner_session = login_user("owner_user", "password123")
    if not owner_session:
        print("❌ Failed to login as owner. Exiting.")
        return
    
    # Login as member
    print("\n🔐 Logging in as member...")
    member_session = login_user("member1", "password123")
    if not member_session:
        print("❌ Failed to login as member. Exiting.")
        return
    
    # Create board as owner
    print("\n📋 Creating test board...")
    board = create_board(owner_session, "Member Management Test Board")
    if not board:
        return
    
    board_id = board['id']
    
    # Test 1: Get initial board members (should be just owner)
    print("\n🧪 Test 1: Get initial board members...")
    members_data = get_board_members(owner_session, board_id)
    if members_data and len(members_data['members']) == 1:
        print("✅ Board has 1 initial member (owner)")
    else:
        print("❌ Board should have 1 initial member")
    
    # Test 2: Owner invites member
    print("\n🧪 Test 2: Owner invites member...")
    if invite_member(owner_session, board_id, "member1"):
        # Check updated member count
        members_data = get_board_members(owner_session, board_id)
        if members_data and len(members_data['members']) == 2:
            print("✅ Board now has 2 members after invitation")
        else:
            print("❌ Board should have 2 members after invitation")
    
    # Test 3: Owner invites another member by email
    print("\n🧪 Test 3: Owner invites member by email...")
    if invite_member(owner_session, board_id, "member2@test.com"):
        members_data = get_board_members(owner_session, board_id)
        if members_data and len(members_data['members']) == 3:
            print("✅ Board now has 3 members after second invitation")
        else:
            print("❌ Board should have 3 members after second invitation")
    
    # Test 4: Try to invite non-existent user
    print("\n🧪 Test 4: Try to invite non-existent user...")
    if not invite_member(owner_session, board_id, "nonexistent@user.com"):
        print("✅ Correctly rejected non-existent user")
    else:
        print("❌ Should not be able to invite non-existent user")
    
    # Test 5: Try to invite same user again
    print("\n🧪 Test 5: Try to invite same user again...")
    if not invite_member(owner_session, board_id, "member1"):
        print("✅ Correctly rejected duplicate invitation")
    else:
        print("❌ Should not be able to invite same user twice")
    
    # Test 6: Non-owner tries to invite member
    print("\n🧪 Test 6: Non-owner tries to invite member...")
    test_non_owner_invite(member_session, board_id, "owner_user")
    
    # Test 7: Owner removes member
    print("\n🧪 Test 7: Owner removes member...")
    members_data = get_board_members(owner_session, board_id)
    if members_data:
        # Find a non-owner member to remove
        member_to_remove = None
        for member in members_data['members']:
            if not member['is_owner']:
                member_to_remove = member
                break
        
        if member_to_remove:
            if remove_member(owner_session, board_id, member_to_remove['id']):
                # Check updated member count
                members_data = get_board_members(owner_session, board_id)
                if members_data and len(members_data['members']) == 2:
                    print("✅ Board now has 2 members after removal")
                else:
                    print("❌ Board should have 2 members after removal")
            else:
                print("❌ Failed to remove member")
        else:
            print("❌ No non-owner member found to remove")
    
    # Test 8: Try to remove owner (should fail)
    print("\n🧪 Test 8: Try to remove board owner...")
    if members_data:
        owner_member = None
        for member in members_data['members']:
            if member['is_owner']:
                owner_member = member
                break
        
        if owner_member:
            # This should fail
            if not remove_member(owner_session, board_id, owner_member['id']):
                print("✅ Correctly prevented removal of board owner")
            else:
                print("❌ Should not be able to remove board owner")
    
    # Test 9: Non-owner tries to remove member
    print("\n🧪 Test 9: Non-owner tries to remove member...")
    if members_data and len(members_data['members']) > 1:
        # Find any member
        member_id = members_data['members'][0]['id']
        response = member_session.delete(f"{API_BASE}/boards/{board_id}/members/{member_id}")
        if response.status_code == 403:
            print("✅ Non-owner correctly blocked from removing members")
        else:
            print(f"❌ Non-owner should not be able to remove members: {response.status_code}")
    
    print("\n✨ Member management tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)