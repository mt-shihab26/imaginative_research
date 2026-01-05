<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

class WelcomeController extends Controller
{
    protected string $basePath = 'cat';

    public function index(Request $request)
    {
        $selected = null;
        $images = null;

        if ($request->has('selected')) {
            $selectedImagePath = $request->input('selected');
            $file = Storage::disk('local')->get("{$this->basePath}/$selectedImagePath");

            $selected = [
                'name' => basename($selectedImagePath),
                'base64' => Str::toBase64($file),
            ];

            $images = $this->getSimilerImages($selectedImagePath);
        } else {
            $images = $this->getRandomImages(50);
        }

        return view('welcome', [
            'selected' => $selected,
            'images' => $images,
        ]);
    }

    protected function getRandomImages(int $limit)
    {
        return collect($this->getAllImagePaths())
            ->shuffle()
            ->take($limit)
            ->map(fn (string $imagePath) => $this->imageToArray($imagePath));
    }

    protected function getSimilerImages(string $selectedImageName)
    {
        // TODO: Implement similarity search with Qdrant
        // For now, return random images excluding the selected one
        return collect($this->getAllImagePaths())
            ->filter(fn ($path) => basename($path) !== $selectedImageName)
            ->shuffle()
            ->take(50)
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
