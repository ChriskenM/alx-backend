#!/usr/bin/node
/*
 *Create a queue with Kue
 */
import kue from 'kue';

// Create a queue
const queue = kue.createQueue();

// Job data
const jobData = {
  phoneNumber: '1234567890',
  message: 'This is a test message',
};

// Create a job in the push_notification_code queue
const job = queue.create('push_notification_code', jobData).save((err) => {
  if (err) {
    console.log('Notification job failed');
  } else {
    console.log(`Notification job created: ${job.id}`);
  }
});

// Add event listeners for job completion and failure
job.on('complete', () => {
  console.log('Notification job completed');
}).on('failed', () => {
  console.log('Notification job failed');
});
