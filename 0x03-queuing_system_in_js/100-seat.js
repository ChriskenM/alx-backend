#!/usr/bin/node
/**
 * Imports and Setup:
 * Import necessary modules: express, kue, redis, and util.
 * Create a Redis client and promisify the get and set methods for async/await usage.
 * Redis Functions:

 * reserveSeat(number): Sets the number of available seats in Redis.
 * getCurrentAvailableSeats(): Gets the current number of available seats from Redis.
 * Initialize Available Seats:

 * Set the initial number of available seats to 50 and initialize the reservationEnabled flag to true.
 * Express Routes:

 * /available_seats: Returns the current number of available seats.
 * /reserve_seat: Creates a job to reserve a seat if reservations are enabled.
 * /process: Processes the queue and reserves seats asynchronously.
 * Queue Processing:

 * Decreases the number of available seats when a job is processed.
 * Disables reservations when no seats are left.
 */

import express from 'express';
import kue from 'kue';
import redis from 'redis';
import { promisify } from 'util';

// Create a Redis client
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Create a Kue queue
const queue = kue.createQueue();

// Reserve seats and get available seats functions
async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return parseInt(seats, 10);
}

// Initialize available seats and reservationEnabled
reserveSeat(50);
let reservationEnabled = true;

// Create an Express app
const app = express();
const port = 1245;

app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    } else {
      return res.json({ status: 'Reservation in process' });
    }
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  }).on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
  });
});

app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats();
    if (availableSeats <= 0) {
      reservationEnabled = false;
      return done(new Error('Not enough seats available'));
    }
    await reserveSeat(availableSeats - 1);
    if (availableSeats - 1 === 0) {
      reservationEnabled = false;
    }
    done();
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
