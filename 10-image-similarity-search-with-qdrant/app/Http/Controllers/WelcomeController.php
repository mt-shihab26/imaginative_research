<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Arr;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

class WelcomeController extends Controller
{
    public function index(Request $request)
    {
        $basePath = 'cat';

        $imagePaths = Storage::disk('local')->files($basePath);
        $imagePaths = Arr::take($imagePaths, 500);

        $selected = null;

        if ($request->has('selected')) {
            $selectedImagePath = $request->input('selected');
            $file = Storage::disk('local')->get("$basePath/$selectedImagePath");

            $selected = [
                'path' => basename($selectedImagePath),
                'base64' => Str::toBase64($file),
            ];
        }

        $images = collect($imagePaths)->map(fn (string $imagePath) => [
            'path' => basename($imagePath),
            'base64' => Str::toBase64(Storage::disk('local')->get($imagePath)),
        ]);

        return view('welcome', [
            'selected' => $selected,
            'images' => collect($images)->take(50),
        ]);
    }
}
