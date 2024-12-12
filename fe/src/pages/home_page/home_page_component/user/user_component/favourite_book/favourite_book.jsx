import React, { useState, useEffect } from 'react';
import './favourite_book.css'; 
import { handleRefreshToken } from '../../../../../auth/login_register';

const FavouriteBooks = () => {
    const [favouriteBooks, setFavouriteBooks] = useState([]); 
    const [loading, setLoading] = useState(false); 
    const [error, setError] = useState(null); 

    // Quản lý trạng thái của modal
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedBookId, setSelectedBookId] = useState(null);

    // Hàm gọi API để lấy danh sách sách yêu thích
    useEffect(() => {
        const fetchFavouriteBooks = async () => {
            setLoading(true);
            setError(null);
            await handleRefreshToken();
            const accessToken = localStorage.getItem('access_token');
            try {

                // Giả lập gọi API
                const response = await fetch('https://librarymanager-aict.onrender.com/user/favorite', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${accessToken}`,
                    },
                });

                if (!response.ok) {
                    throw new Error('Không thể tải được sách.');
                }

                const data = await response.json();
                setFavouriteBooks(data.books || []);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchFavouriteBooks();
    }, []);

    // Hàm mở modal khi nhấn nút "Xóa"
    const openModal = (id) => {
        setSelectedBookId(id);
        setIsModalOpen(true);
    };

    // Hàm đóng modal
    const closeModal = () => {
        setIsModalOpen(false);
        setSelectedBookId(null);
    };

    // Hàm gọi API để xóa sách yêu thích
    const handleDeleteBook = async () => {
        try {
            await handleRefreshToken();
            const accessToken = localStorage.getItem('access_token');
            const response = await fetch(`https://librarymanager-aict.onrender.com/user/favorite/${selectedBookId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${accessToken}`,
                },
            });
            if(response.ok){

            }

            if (!response.ok) {
                throw new Error('Không thể xóa sách.');
            }

            setFavouriteBooks(favouriteBooks.filter(book => book.id !== selectedBookId));
            closeModal(); // Đóng modal sau khi xóa thành công
        } catch (err) {
            setError(err.message);
        }
    };

    // Hiển thị trạng thái
    if (loading) {
        return <div>Đang tải dữ liệu...</div>;
    }

    if (error) {
        return <div style={{ color: 'black' }}>{error}</div>;
    }

    if (favouriteBooks.length === 0) {
        return <div>Không có sách yêu thích để hiển thị.</div>;
    }

    return (
        <div className="table-container">
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Tên Sách</th>
                        <th>Hình ảnh</th>
                        <th>Hành động</th>
                    </tr>
                </thead>
                <tbody>
                    {favouriteBooks.map((book,index) => (
                        <tr key={book.id}>
                            <td>{index+1}</td>
                            <td>{book.title}</td>
                            <td className="image-column">
                                <img src={book.url_image || 'https://via.placeholder.com/150'} alt={book.title} />
                            </td>
                            <td>
                                <button 
                                    onClick={() => openModal(book.id)} 
                                    className="delete-button"
                                >
                                    Xóa
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {/* Modal xác nhận xóa */}
            {isModalOpen && (
                <div className="modal">
                    <div className="modal-content-fabook">
                        <h3>Bạn chắc chắn muốn xóa sách này chứ?</h3>
                        <div className="modal-buttons">
                            <button onClick={closeModal} className="cancel-button">
                                Không
                            </button>
                            <button onClick={handleDeleteBook} className="confirm-button">
                                Đồng ý
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default FavouriteBooks;