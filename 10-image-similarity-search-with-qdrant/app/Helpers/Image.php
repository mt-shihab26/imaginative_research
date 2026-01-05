<?php

namespace App\Helpers;

use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

class Image
{
    protected string $basePath = 'cat';

    public function getImageFile(string $imagePath)
    {
        return Storage::disk('local')->get("{$this->basePath}/$imagePath");
    }

    public function getSimilerImages(string $selectedImageName)
    {
        // TODO: Implement similarity search with Qdrant
        // For now, return random images excluding the selected one
        return collect($this->getAllImagePaths())
            ->filter(fn ($path) => basename($path) !== $selectedImageName)
            ->shuffle()
            ->take(50)
            ->map(fn (string $imagePath) => $this->imageToArray($imagePath));
    }

    public function getRandomImages(int $limit)
    {
        return collect($this->getAllImagePaths())
            ->shuffle()
            ->take($limit)
            ->map(fn (string $imagePath) => $this->imageToArray($imagePath));
    }

    protected function getAllImagePaths(): array
    {
        return Storage::disk('local')->files($this->basePath);
    }

    protected function imageToArray(string $imagePath): array
    {
        return [
            'name' => basename($imagePath),
            'base64' => Str::toBase64(Storage::disk('local')->get($imagePath)),
        ];
    }
}
