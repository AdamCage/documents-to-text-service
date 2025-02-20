import math

import numpy as np
import cv2

from .abstract_classes import ImageProcessor


class GrayscaleConverter(ImageProcessor):
    """Класс для преобразования изображения в оттенки серого."""
    
    def process(self, image: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


class AdaptiveBinarizer(ImageProcessor):
    """Класс для адаптивной бинаризации изображения с использованием гауссового адаптивного порога."""

    block_size = 5
    C = 1.1
    
    def process(self, image: np.ndarray) -> np.ndarray:
        binary = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, self.block_size, self.C)

        return binary


class Denoiser(ImageProcessor):
    """Класс для устранения шума на изображении."""

    kernel_size = (5, 5)
    sigma = 0

    def process(self, image: np.ndarray) -> np.ndarray:
        return cv2.GaussianBlur(image, self.kernel_size, self.sigma)


class Deskewer(ImageProcessor):
    """Класс для коррекции наклона изображения."""
    
    def process(self, image: np.ndarray) -> np.ndarray:
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        angle = -(90 + angle) if angle < -45 else -angle

        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)

        return cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


class AutoCropper(ImageProcessor):
    """Класс для автоматического выравнивания перспективы и обрезки текста."""

    def process(self, image: np.ndarray) -> np.ndarray:
        edges = cv2.Canny(image, 50, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return image

        contour = max(contours, key=cv2.contourArea)

        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:
            pts = approx.reshape(4, 2)

            rect = np.zeros((4, 2), dtype="float32")
            s = pts.sum(axis=1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]
            diff = np.diff(pts, axis=1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]

            (tl, tr, br, bl) = rect
            widthA = np.linalg.norm(br - bl)
            widthB = np.linalg.norm(tr - tl)
            maxWidth = max(int(widthA), int(widthB))
            heightA = np.linalg.norm(tr - br)
            heightB = np.linalg.norm(tl - bl)
            maxHeight = max(int(heightA), int(heightB))
            
            dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype="float32")
            M = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

            return warped

        return image
    

class ContrastEnhancer(ImageProcessor):
    """Класс для повышения контрастности изображения с использованием CLAHE."""

    clip_limit = 1.1
    tile_grid_size = (4, 4)


    def process(self, image: np.ndarray) -> np.ndarray:
        if len(image.shape) == 2 or (len(image.shape) == 3 and image.shape[2] == 1):
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(clipLimit=self.clip_limit, tileGridSize=self.tile_grid_size)
        l = clahe.apply(l)

        lab = cv2.merge((l, a, b))
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        return enhanced
        

class SharpnessEnhancer(ImageProcessor):
    """Класс для повышения резкости изображения с использованием фильтрации."""

    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    

    def process(self, image: np.ndarray) -> np.ndarray:
        sharpened = cv2.filter2D(image, -1, self.kernel)

        return sharpened


class RotationCorrector(ImageProcessor):
    """Класс для коррекции угла поворота изображения на основе обнаруженных линий.
    За основу взято:
        - статья: https://newtechaudit.ru/avtomaticheskaya-korrekcziya-ugla-povorota-izobrazheniya-v-zadache-raspoznavaniya-teksta/
        - код: https://github.com/reIkaros/img_rotate/blob/main/rotate.ipynb
    """

    def process(self, image: np.ndarray) -> np.ndarray:
        # Преобразование изображения в градации серого
        src = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        final = image.copy()

        # Очистка от шумов
        im_bw = cv2.adaptiveThreshold(src, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 10)

        # Используем оригинальный размер для обработки
        resized = im_bw  # Оставляем изображение без изменения размера

        # Выделение границ Кэнни
        dst = cv2.Canny(resized, 400, 100)

        # Преобразование Хаффа
        linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, None, 20, 10)

        coner_array = []
        if linesP is not None:
            for i in range(len(linesP)):
                l = linesP[i][0]
                coner_array.append(math.degrees(math.atan2(l[3] - l[1], l[2] - l[0])))

        if coner_array:
            coner = np.mean(coner_array)
            (h, w) = src.shape[:2]
            center = (w / 2, h / 2)
            M = cv2.getRotationMatrix2D(center, coner, 1.0)
            rotated = cv2.warpAffine(final, M, (w, h), borderMode=cv2.BORDER_REPLICATE)

            return rotated
        
        else:
            return final
