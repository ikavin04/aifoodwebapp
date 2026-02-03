"""Add user addresses and update restaurant with city

Revision ID: add_user_addresses
Revises: 0851a9d37d9f
Create Date: 2026-02-03

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_user_addresses'
down_revision = '0851a9d37d9f'
branch_labels = None
depends_on = None


def upgrade():
    # Create user_addresses table
    op.create_table('user_addresses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('label', sa.String(length=50), nullable=False),
        sa.Column('address_line1', sa.String(length=255), nullable=False),
        sa.Column('address_line2', sa.String(length=255), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=False),
        sa.Column('state', sa.String(length=100), nullable=False),
        sa.Column('pincode', sa.String(length=20), nullable=False),
        sa.Column('landmark', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('is_default', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add current_address_id to users table
    op.add_column('users', sa.Column('current_address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_users_current_address', 'users', 'user_addresses', ['current_address_id'], ['id'])
    
    # Add city, state, pincode to restaurants table
    op.add_column('restaurants', sa.Column('city', sa.String(length=100), nullable=True))
    op.add_column('restaurants', sa.Column('state', sa.String(length=100), nullable=True))
    op.add_column('restaurants', sa.Column('pincode', sa.String(length=20), nullable=True))
    
    # Update existing restaurants with default city (you can modify this)
    op.execute("UPDATE restaurants SET city = 'Mumbai', state = 'Maharashtra', pincode = '400001' WHERE city IS NULL")
    
    # Make city NOT NULL after setting default values
    op.alter_column('restaurants', 'city', nullable=False)


def downgrade():
    # Remove columns from restaurants
    op.drop_column('restaurants', 'pincode')
    op.drop_column('restaurants', 'state')
    op.drop_column('restaurants', 'city')
    
    # Remove current_address_id from users
    op.drop_constraint('fk_users_current_address', 'users', type_='foreignkey')
    op.drop_column('users', 'current_address_id')
    
    # Drop user_addresses table
    op.drop_table('user_addresses')
