<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;

class UploadEmbedding extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'app:upload-embedding';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Generate and upload embedding to Qdrant';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        //
    }
}
