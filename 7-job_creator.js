import kue from 'kue';

const jobs = [
  // ... (same as Task 6)
];

const queue = kue.createQueue();

jobs.forEach((jobData, index) => {
  const job = queue.create('push_notification_code_2', jobData);

  job.save((err) => {
    if (!err) console.log(`Notification job created: ${job.id}`);
  });

  job.on('complete', () => {
    console.log(`Notification job ${job.id} completed`);
  });

  job.on('failed', (err) => {
    console.log(`Notification job ${job.id} failed: ${err}`);
  });

  job.on('progress', (progress) => {
    console.log(`Notification job ${job.id} ${progress}% complete`);
  });
});
