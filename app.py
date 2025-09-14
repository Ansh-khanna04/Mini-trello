#!/usr/bin/env python3
import os
from flask import Flask
from app import create_app, db, socketio
from swagger_ui import init_swagger_ui

def create_demo_data():
    """Create demo data for testing"""
    from app.models import User, Board, List, Card
    
    # Create demo user
    demo_user = User.query.filter_by(username='demo').first()
    if not demo_user:
        demo_user = User(
            username='demo',
            email='demo@minitrollo.com',
            name='Demo User'
        )
        demo_user.set_password('demo123')
        db.session.add(demo_user)
        db.session.commit()
        print("Created demo user (username: demo, password: demo123)")
    
    # Create demo board
    demo_board = Board.query.filter_by(title='Demo Project Board').first()
    if not demo_board:
        demo_board = Board(
            title='Demo Project Board',
            description='A sample board to demonstrate Mini Trello features',
            owner_id=demo_user.id,
            background_color='#0079bf'
        )
        demo_board.members.append(demo_user)
        db.session.add(demo_board)
        db.session.flush()
        
        # Create demo lists
        lists_data = [
            ('Backlog', 0),
            ('In Progress', 1),
            ('Review', 2),
            ('Done', 3)
        ]
        
        demo_lists = {}
        for title, position in lists_data:
            demo_list = List(
                title=title,
                position=float(position),
                board_id=demo_board.id
            )
            db.session.add(demo_list)
            db.session.flush()
            demo_lists[title] = demo_list
        
        # Create demo cards
        cards_data = [
            ('Backlog', [
                'Set up project infrastructure',
                'Design user interface mockups',
                'Plan database schema'
            ]),
            ('In Progress', [
                'Implement user authentication',
                'Create board view components'
            ]),
            ('Review', [
                'Add drag and drop functionality'
            ]),
            ('Done', [
                'Set up development environment',
                'Create project documentation'
            ])
        ]
        
        for list_name, card_titles in cards_data:
            list_obj = demo_lists[list_name]
            for i, title in enumerate(card_titles):
                card = Card(
                    title=title,
                    position=float(i),
                    list_id=list_obj.id
                )
                db.session.add(card)
        
        db.session.commit()
        print(f"Created demo board '{demo_board.title}' with sample data")

if __name__ == '__main__':
    app = create_app()
    
    # Initialize Swagger UI
    init_swagger_ui(app)
    
    with app.app_context():
        # Create database tables
        db.create_all()
        print("Database tables created successfully")
        
        # Create demo data
        create_demo_data()
    
    print("\n" + "="*50)
    print("🚀 Mini Trello is starting!")
    print("="*50)
    print("📋 Demo login credentials:")
    print("   Username: demo")
    print("   Password: demo123")
    print("="*50)
    print("🌐 Access the application at:")
    print("   Main App:  http://localhost:5000")
    print("   API Docs:  http://localhost:5000/docs")
    print("="*50)
    print("✨ Features included:")
    print("   • User authentication (signup/login)")
    print("   • Kanban board with drag & drop")
    print("   • Real-time collaboration")
    print("   • Card management & comments")
    print("   • Activity tracking")
    print("   • Search & filtering")
    print("="*50 + "\n")
    
    # Run the application with SocketIO
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)