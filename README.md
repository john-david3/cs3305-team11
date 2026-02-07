# **Team 11 - Gander - Live Streaming Platform**

## Overview and Purpose

Gander is a live streaming platform created as a 3rd year team software project as part of UCC's Computer Science degree. It provides a source of entertainment and a community for users with similar interests. Users can watch live streams from other users, whether gaming or IRL, or broadcast their own content. By clicking the "Go Live" button, a logged-in user is presented with a dashboard where they can set their stream's title, category, and thumbnail. Users watching a live stream can interact with other viewers and the streamer through a live chat. Users can also subscribe to their favourite streamers via the Stripe API on a monthly basis.

![Screenshot 2025-03-03 123446](https://github.com/user-attachments/assets/a23c2974-9500-492d-be07-91161606e805)

![Screenshot 2025-03-03 125748](https://github.com/user-attachments/assets/ab2092a3-c599-4a90-a616-f08faa4c76ba)

## Access Control Levels

The platform implements three-tier access control:

1. **No Access** (Non-authenticated Users)
   - View live streams
   - Browse available content

2. **Regular Access** (Authenticated Users)
   - All features available to non-authenticated users
   - Donate to streamers through Stripe integration
   - Interact with streams through comments
   - Follow other users
   - Become a content creator and start streaming

3. **Admin Access**
   - Full platform management capabilities
   - Content moderation tools
   - User account management
   - System configuration controls

![Screenshot 2025-03-03 122943](https://github.com/user-attachments/assets/26b82756-3e39-41d3-8d30-b3a6cbda21a0)

## Technical Stack

### Frontend

- React with TypeScript for type safety
- Tailwind CSS for styling
- Video.js for stream playback
- Stripe integration for payment processing

### Backend

- Python with Flask web framework
- SQLite database for data persistence
- Flask-Session for user session management
- Nginx RTMP module for stream handling

### Infrastructure

- Docker for containerization and deployment
- Docker Compose for multi-container orchestration
- Nginx for reverse proxy and RTMP streaming server
- Microservices architecture

## Development

This project was maintained on GitHub, with all team members contributing through version control. The team followed collaborative development practices including regular code reviews and feature branches.

## Future Development

Development on Gander has concluded. Potential extensions that were not implemented include:

- **User Profiles**: Customizable profiles showcasing streaming history, followers, and personal information.
- **Enhanced Chat Features**: Emojis, chat moderation tools, and the ability to pin messages during live streams.
- **Mobile Application**: A mobile app built with React Native to allow users to watch and stream on the go.
- **Monetization Options**: Additional revenue streams for content creators, such as merchandise sales or one-time donations.
- **Analytics Dashboard**: A dashboard for streamers to track viewership, engagement metrics, and revenue over time.

## Running the Project

Pre-requisites:

- [Docker](https://docs.docker.com/get-docker/) (includes Docker Compose)
- Node.js & npm (optional, for local frontend development)

Steps:

1. Rename the following `.env.example` files to `.env` and fill in the required values:
   - `frontend/.env.example` — React frontend variables
   - `web_server/.env.example` — Flask backend variables
2. Start all services with Docker Compose:

   ```bash
   docker compose up --build
   ```

   > **Note:** Older versions of Docker use `docker-compose` (with a hyphen) instead of `docker compose` (with a space).
3. Access the frontend at `localhost:8080` in your browser. Note that the terminal output from Vite will show `localhost:5173` — this is the internal container port. Nginx exposes the application on port `8080`.
