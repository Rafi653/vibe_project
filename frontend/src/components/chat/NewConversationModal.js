/**
 * NewConversationModal Component
 * Modal for creating new conversations
 */

import React, { useState } from 'react';
import './Chat.css';

const NewConversationModal = ({ onClose, onCreate, users }) => {
    const [conversationType, setConversationType] = useState('direct');
    const [selectedUsers, setSelectedUsers] = useState([]);
    const [groupName, setGroupName] = useState('');
    const [searchTerm, setSearchTerm] = useState('');

    const currentUserId = JSON.parse(localStorage.getItem('user'))?.id;
    const filteredUsers = users.filter(user => 
        user.id !== currentUserId && 
        user.full_name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handleUserToggle = (userId) => {
        if (conversationType === 'direct') {
            setSelectedUsers([userId]);
        } else {
            setSelectedUsers(prev =>
                prev.includes(userId)
                    ? prev.filter(id => id !== userId)
                    : [...prev, userId]
            );
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        
        if (selectedUsers.length === 0) {
            alert('Please select at least one user');
            return;
        }

        if (conversationType === 'group' && !groupName.trim()) {
            alert('Please enter a group name');
            return;
        }

        onCreate({
            conversation_type: conversationType,
            participant_ids: selectedUsers,
            name: conversationType === 'group' ? groupName : null,
        });
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h3>New Conversation</h3>
                    <button onClick={onClose} className="btn-close">×</button>
                </div>
                
                <form onSubmit={handleSubmit} className="modal-body">
                    <div className="form-group">
                        <label>Conversation Type</label>
                        <select
                            value={conversationType}
                            onChange={(e) => {
                                setConversationType(e.target.value);
                                setSelectedUsers([]);
                            }}
                            className="form-control"
                        >
                            <option value="direct">Direct Message</option>
                            <option value="group">Group Chat</option>
                        </select>
                    </div>

                    {conversationType === 'group' && (
                        <div className="form-group">
                            <label>Group Name</label>
                            <input
                                type="text"
                                value={groupName}
                                onChange={(e) => setGroupName(e.target.value)}
                                placeholder="Enter group name"
                                className="form-control"
                            />
                        </div>
                    )}

                    <div className="form-group">
                        <label>Search Users</label>
                        <input
                            type="text"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            placeholder="Search by name..."
                            className="form-control"
                        />
                    </div>

                    <div className="form-group">
                        <label>
                            Select {conversationType === 'direct' ? 'User' : 'Users'}
                        </label>
                        <div className="user-list">
                            {filteredUsers.length === 0 ? (
                                <p className="no-users">No users found</p>
                            ) : (
                                filteredUsers.map((user) => (
                                    <div
                                        key={user.id}
                                        className={`user-item ${selectedUsers.includes(user.id) ? 'selected' : ''}`}
                                        onClick={() => handleUserToggle(user.id)}
                                    >
                                        <div className="user-avatar">{user.full_name[0]}</div>
                                        <div className="user-info">
                                            <span className="user-name">{user.full_name}</span>
                                            <span className="user-role">{user.role}</span>
                                        </div>
                                        {selectedUsers.includes(user.id) && (
                                            <span className="selected-checkmark">✓</span>
                                        )}
                                    </div>
                                ))
                            )}
                        </div>
                    </div>

                    <div className="modal-footer">
                        <button type="button" onClick={onClose} className="btn-secondary">
                            Cancel
                        </button>
                        <button type="submit" className="btn-primary">
                            Create Conversation
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default NewConversationModal;
