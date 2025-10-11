"""Initial migration with user and fitness models

Revision ID: 001
Revises: 
Create Date: 2025-10-11 00:31:01.870000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('client', 'coach', 'admin', name='userrole'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Create workout_logs table
    op.create_table(
        'workout_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('workout_date', sa.Date(), nullable=False),
        sa.Column('exercise_name', sa.String(length=255), nullable=False),
        sa.Column('sets', sa.Integer(), nullable=True),
        sa.Column('reps', sa.Integer(), nullable=True),
        sa.Column('weight', sa.Float(), nullable=True),
        sa.Column('duration_minutes', sa.Integer(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workout_logs_id'), 'workout_logs', ['id'], unique=False)
    op.create_index(op.f('ix_workout_logs_user_id'), 'workout_logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_workout_logs_workout_date'), 'workout_logs', ['workout_date'], unique=False)

    # Create diet_logs table
    op.create_table(
        'diet_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('meal_date', sa.Date(), nullable=False),
        sa.Column('meal_type', sa.Enum('breakfast', 'lunch', 'dinner', 'snack', name='mealtype'), nullable=False),
        sa.Column('food_name', sa.String(length=255), nullable=False),
        sa.Column('calories', sa.Float(), nullable=True),
        sa.Column('protein_grams', sa.Float(), nullable=True),
        sa.Column('carbs_grams', sa.Float(), nullable=True),
        sa.Column('fat_grams', sa.Float(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_diet_logs_id'), 'diet_logs', ['id'], unique=False)
    op.create_index(op.f('ix_diet_logs_user_id'), 'diet_logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_diet_logs_meal_date'), 'diet_logs', ['meal_date'], unique=False)

    # Create workout_plans table
    op.create_table(
        'workout_plans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('status', sa.Enum('active', 'completed', 'paused', 'cancelled', name='planstatus'), nullable=False),
        sa.Column('duration_weeks', sa.Integer(), nullable=True),
        sa.Column('workout_details', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_workout_plans_id'), 'workout_plans', ['id'], unique=False)
    op.create_index(op.f('ix_workout_plans_user_id'), 'workout_plans', ['user_id'], unique=False)

    # Create diet_plans table
    op.create_table(
        'diet_plans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('status', sa.Enum('active', 'completed', 'paused', 'cancelled', name='planstatus'), nullable=False),
        sa.Column('target_calories', sa.Float(), nullable=True),
        sa.Column('target_protein_grams', sa.Float(), nullable=True),
        sa.Column('target_carbs_grams', sa.Float(), nullable=True),
        sa.Column('target_fat_grams', sa.Float(), nullable=True),
        sa.Column('meal_plan_details', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_diet_plans_id'), 'diet_plans', ['id'], unique=False)
    op.create_index(op.f('ix_diet_plans_user_id'), 'diet_plans', ['user_id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f('ix_diet_plans_user_id'), table_name='diet_plans')
    op.drop_index(op.f('ix_diet_plans_id'), table_name='diet_plans')
    op.drop_table('diet_plans')
    
    op.drop_index(op.f('ix_workout_plans_user_id'), table_name='workout_plans')
    op.drop_index(op.f('ix_workout_plans_id'), table_name='workout_plans')
    op.drop_table('workout_plans')
    
    op.drop_index(op.f('ix_diet_logs_meal_date'), table_name='diet_logs')
    op.drop_index(op.f('ix_diet_logs_user_id'), table_name='diet_logs')
    op.drop_index(op.f('ix_diet_logs_id'), table_name='diet_logs')
    op.drop_table('diet_logs')
    
    op.drop_index(op.f('ix_workout_logs_workout_date'), table_name='workout_logs')
    op.drop_index(op.f('ix_workout_logs_user_id'), table_name='workout_logs')
    op.drop_index(op.f('ix_workout_logs_id'), table_name='workout_logs')
    op.drop_table('workout_logs')
    
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    
    # Drop enums
    sa.Enum(name='userrole').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='mealtype').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='planstatus').drop(op.get_bind(), checkfirst=True)
