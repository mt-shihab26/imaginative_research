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
        $imagePaths = Storage::disk('local')->files('cat');
        $imagePaths = Arr::take($imagePaths, 10);

        $selectedImage = null;

        if ($request->has('selected_image')) {
            $selectedImagePath = $request->input('selected_image');
            $file = Storage::disk('local')->get($selectedImagePath);

            $selectedImage = [
                'path' => $selectedImagePath,
                'base64' => Str::toBase64($file),
            ];
        }

        $images = collect($imagePaths)->map(function (string $imagePath) {
            $file = Storage::disk('local')->get($imagePath);

            return [
                'path' => $imagePath,
                'base64' => Str::toBase64($file),
            ];
        });

        return view('welcome', [
            'selectedImage' => $selectedImage,
            'images' => $images,
        ]);
    }
}
